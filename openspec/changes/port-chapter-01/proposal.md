## Why

Chapter 1 sets the pattern for the whole book: the first functional test, the first running server, and the first git commit. It is also the first real use of the conventions fixed in `foundation-quart-stack` (uv-only setup, Quart, Hypercorn, Playwright, snapshots as plain directories). It must be ported first and approved before any later chapter builds on it.

This change depends on `foundation-quart-stack`, which defines the project layout, the test stack, the front-end stance and the chapter-verification rules that apply here. It should be applied after that change is complete.

## What Changes

- Rewrite `chapter_01.asciidoc` ("Getting Django Set Up Using a Functional Test") for the new stack, keeping its three-part structure: write a failing functional test first, get the app running, then start a git repository.
- Replace the Selenium and `webdriver.Firefox()` first test with a Playwright test in Chromium, which fails because nothing is serving the page.
- Replace the Django project setup (`django-admin startproject`, `manage.py runserver`) with a uv project (`uv init`, `uv add quart hypercorn`) and a minimal Quart app run with Hypercorn.
- Replace the virtualenv and `pip install` instructions with uv commands only.
- Add the chapter-1 snapshot at `source/chapter_01/` as a plain directory, and remove the old `source/chapter_01/superlists` git submodule entry.
- Add `tests/test_chapter_01.py` as a `UvChapterTest` subclass that replays the new chapter, replacing the Django-era test of the same name.
- Update the repository's CI matrix entry for chapter 1 to run the new test.
- Decide, in the design, how the first functional test reaches the app before a live-server fixture is introduced, since the foundation's fixture arrives later in the book.

## Capabilities

### New Capabilities
- `chapter-01-first-test-and-server`: What chapter 1 teaches and delivers: a first failing functional test, a running Quart app served by Hypercorn, a git repository, and a verified chapter snapshot.

### Modified Capabilities
<!-- None: foundation-quart-stack's capabilities are not changed, only used. -->

## Impact

- Rewrites `chapter_01.asciidoc` and `tests/test_chapter_01.py`.
- Adds `source/chapter_01/` as plain files and removes the matching submodule entry from `.gitmodules`.
- Touches the CI workflow's chapter-1 entry and the `test_chapter_01` Makefile target.
- Leaves chapters 2 onward unchanged, so their tests keep using the Django-era harness until they are ported.
- Requires `asciidoctor` and Chromium to be installed to build and verify the chapter.
