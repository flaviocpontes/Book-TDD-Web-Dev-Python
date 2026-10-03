#!/usr/bin/env python3
import socket
import subprocess
import time

from book_parser import CodeListing, Command
from uv_chapter_test import UvChapterTest

DEV_SERVER_PORT = 8000


def wait_until_listening(port, timeout=10):
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        try:
            socket.create_connection(("127.0.0.1", port), timeout=0.2).close()
            return
        except OSError:
            time.sleep(0.1)
    raise AssertionError(f"dev server did not start listening on port {port}")


class Chapter1Test(UvChapterTest):
    chapter_name = "chapter_01"
    previous_chapter = None

    def setUp(self):
        super().setUp()
        self.dev_server = None

    def tearDown(self):
        self.stop_dev_server()
        super().tearDown()

    def start_dev_server(self):
        # The server command never returns, so SourceTree.run_command (which only
        # knows to leave "runserver" running) can't be used: start it ourselves.
        with socket.socket() as sock:
            if sock.connect_ex(("127.0.0.1", DEV_SERVER_PORT)) == 0:
                self.fail(f"port {DEV_SERVER_PORT} is already in use")
        self.dev_server = subprocess.Popen(
            "uv run hypercorn superlists:app",
            shell=True,
            cwd=self.tempdir,
            executable="/bin/bash",
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            start_new_session=True,
        )
        wait_until_listening(DEV_SERVER_PORT)

    def stop_dev_server(self):
        if self.dev_server is None:
            return
        import os
        import signal

        try:
            os.killpg(self.dev_server.pid, signal.SIGTERM)
        except ProcessLookupError:
            pass
        self.dev_server.wait(timeout=10)
        self.dev_server = None

    def test_listings_and_commands_and_output(self):
        self.parse_listings()
        self.start_from_previous_snapshot()

        # The harness runs every command in the temp dir, which has no
        # "superlists" folder to cd into: create the project in place instead.
        self.replace_command_with_check(
            0, "superlists", "--name superlists ."
        )
        self.skip_with_check(1, "cd superlists")

        # The dev server is started by hand below, so skip it and its output
        self.skip_with_check(10, "hypercorn superlists:app")
        self.listings[11].skip = True

        # sanity checks
        self.assertEqual(type(self.listings[6]), CodeListing)
        self.assertEqual(type(self.listings[7]), Command)

        while self.pos < len(self.listings):
            if self.pos == 12:
                self.start_dev_server()
            self.recognise_listing_and_process_it()
        self.stop_dev_server()

        self.assert_all_listings_checked(self.listings)

        self.check_final_diff(
            ignore=[
                "name =",  # author details from the reader's git config
                ">=",  # dependency lower bounds drift as new releases appear
            ]
        )
