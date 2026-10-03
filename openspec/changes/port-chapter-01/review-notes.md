# Chapter 1 review notes

Read `chapter_01.html` (build with `make chapter_01.html`), then run `make test_chapter_01`.

- Tooling: uv 0.12.5, Python 3.14, Quart, Hypercorn, pytest-playwright, Chromium.
- `uv init --lib --python 3.14`: uv's default Python is 3.12, so the flag is needed.
- The first FT is a pytest test (`tests/functional/test_first_visit.py`), not a standalone script. It expects a server on `http://localhost:8000` that the reader starts in a second shell. The live-server fixture is for a later chapter.
- Dropped: the "Firefox upgrade pop-up" aside (no Chromium equivalent), the Django screenshot of "It worked!" (replaced by a sentence), the "Oops, .pyc files" git detour (uv's `.gitignore` already covers them), and the `git init` step (uv already did it).
- Added: a short "set up the project with uv" section before the first test, and a one-paragraph explanation of `async def`.
- Unused now: `images/tdd3_0102.png` and `images/tdd3_0103.png`.
- Test deviations: the chapter test creates the project in place instead of `cd superlists`, starts Hypercorn itself, and ignores author details and `>=` lower bounds in `pyproject.toml` in the final snapshot diff. The snapshot's `pyproject.toml` carries the maintainer's git name and email in `authors`.
- Not verified: the new CI step (`uvx playwright install-deps chromium`) has not run on a real GitHub runner. The Makefile `test_chapter_01` target needed no change.
- Cross-references from other chapters to chapter 1 content were not touched.
