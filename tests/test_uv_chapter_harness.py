import subprocess
import tempfile
from pathlib import Path

from book_parser import CodeListing, Command, Output
from uv_chapter_test import UvChapterTest

DEMO = Path(__file__).parent / "uv_harness_demo"
DEMO_TEXT = (DEMO / "chapter_demo.asciidoc").read_text()


class DemoChapterTest(UvChapterTest):
    """Builds the demo chapter's HTML (optionally with text altered) and replays it."""

    chapter_name = "chapter_demo"
    snapshots_dir = DEMO / "source"
    asciidoc_text = DEMO_TEXT

    def setUp(self):
        super().setUp()
        self.book_dir = Path(tempfile.mkdtemp())
        source = self.book_dir / f"{self.chapter_name}.asciidoc"
        source.write_text(self.asciidoc_text)
        subprocess.run(
            ["asciidoctor", "-a", "!example-caption", str(source)],
            check=True,
            capture_output=True,
        )

    def replay(self):
        self.parse_listings()
        self.start_from_previous_snapshot()
        while self.pos < len(self.listings):
            self.recognise_listing_and_process_it()
        self.assert_all_listings_checked(self.listings)
        self.check_final_diff()


class UvChapterHarnessTest(DemoChapterTest):
    def test_parses_two_listings_and_replays_with_uv(self):
        self.parse_listings()
        self.assertEqual(
            [type(x) for x in self.listings], [CodeListing, Command, Output]
        )
        self.replay()


class AlteredListingFailsTest(DemoChapterTest):
    """Text changed, snapshot not updated: the chapter test must fail."""

    asciidoc_text = DEMO_TEXT.replace('print("Hello, uv")', 'print("Hello, UV")', 1)

    def test_changed_listing_is_caught(self):
        # the command's output still says "Hello, uv", so the replay itself fails
        with self.assertRaises(AssertionError):
            self.replay()


class AlteredSnapshotFailsTest(DemoChapterTest):
    """Listing and output agree, but the snapshot differs: final diff must fail."""

    asciidoc_text = DEMO_TEXT.replace("Hello, uv", "Hello, UV")

    def test_listing_that_drifts_from_snapshot_is_caught(self):
        with self.assertRaises(AssertionError) as caught:
            self.replay()
        self.assertIn("Hello, UV", str(caught.exception))


class AlteredOutputFailsTest(DemoChapterTest):
    asciidoc_text = DEMO_TEXT.replace("\nHello, uv\n----", "\nGoodbye, uv\n----")

    def test_changed_output_is_caught(self):
        with self.assertRaises(AssertionError):
            self.replay()


class PreviousSnapshotTest(DemoChapterTest):
    previous_chapter = "chapter_demo_prev"

    def test_starts_from_a_plain_copy_of_the_previous_snapshot(self):
        self.parse_listings()
        self.start_from_previous_snapshot()
        self.assertEqual(
            (self.tempdir / "hello.py").read_text(), 'print("Hello, uv")\n'
        )
        self.assertFalse((self.tempdir / ".git").exists())
