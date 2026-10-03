"""Chapter test base class for the uv/Quart edition of the book.

Replays a chapter's listings and commands in a clean temp directory, like
ChapterTest, but without Django, Selenium or git-submodule snapshots:

* the chapter starts from a plain copy of the previous chapter's snapshot,
* commands are run as written (uv, uv run ...), with no manual virtualenv,
* the end state is compared against source/<chapter>/ with a directory diff.
"""

import os
import shutil
import subprocess
from pathlib import Path

from book_tester import ChapterTest
from lxml import html
from book_parser import parse_listing

REPO_ROOT = Path(__file__).parent.parent
SNAPSHOT_IGNORE = shutil.ignore_patterns(
    ".venv", "__pycache__", ".pytest_cache", ".git", "*.pyc", ".ruff_cache"
)
DIFF_EXCLUDES = [".venv", "__pycache__", ".pytest_cache", ".git", "*.pyc", "uv.lock"]


class UvChapterTest(ChapterTest):
    chapter_name = "override me"
    previous_chapter: str | None = None
    # where <chapter_name>.html is built, and where source/<chapter>/ snapshots live
    book_dir: Path = REPO_ROOT
    snapshots_dir: Path = REPO_ROOT / "source"

    def setUp(self):
        super().setUp()
        # the harness itself may run inside another venv: stop uv from seeing it
        self._saved_env = {
            k: os.environ.pop(k, None) for k in ("VIRTUAL_ENV", "UV_PROJECT_ENVIRONMENT")
        }

    def tearDown(self):
        super().tearDown()
        for key, value in self._saved_env.items():
            if value is not None:
                os.environ[key] = value

    def parse_listings(self):
        raw_html = (self.book_dir / f"{self.chapter_name}.html").read_text(
            encoding="utf-8"
        )
        all_nodes = html.fromstring(raw_html).cssselect(
            ".exampleblock.sourcecode, div:not(.sourcecode) div.listingblock"
        )
        listing_nodes = []
        for ix, node in enumerate(all_nodes):
            prev = all_nodes[ix - 1]
            if node not in list(prev.iterdescendants()):
                listing_nodes.append(node)
        self.listings = [p for n in listing_nodes for p in parse_listing(n)]

    def start_from_previous_snapshot(self):
        """Copy the previous chapter's snapshot into the temp dir (plain copy,
        no git)."""
        if self.previous_chapter is None:
            return
        shutil.copytree(
            self.snapshots_dir / self.previous_chapter,
            self.tempdir,
            ignore=SNAPSHOT_IGNORE,
            dirs_exist_ok=True,
        )

    def snapshot_diff(self) -> str:
        """Unified diff, ignoring whitespace, of the temp dir against the
        chapter snapshot. Empty string means they match."""
        cmd = ["diff", "-ruw"]
        for pattern in DIFF_EXCLUDES:
            cmd += ["-x", pattern]
        cmd += [str(self.snapshots_dir / self.chapter_name), str(self.tempdir)]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode not in (0, 1):
            self.fail(f"diff failed: {result.stderr}")
        return result.stdout

    def check_final_diff(self, ignore=None):
        diff = self.snapshot_diff()
        if "Only in" in diff:
            self.fail(f"Files differ from snapshot:\n{diff}")
        super().check_final_diff(ignore=ignore, diff=diff)
