## 1. Prerequisites and facts to check

- [x] 1.1 Install `asciidoctor` and verify `make chapter_01.html` builds the current chapter's HTML
- [x] 1.2 Run `uv init --package superlists` in a scratch directory outside the repo, record the uv version, and note whether it creates a git repository, `.gitignore`, `README.md` and a lock file (answers the design's open question)
- [x] 1.3 In the scratch project, start `uv run hypercorn superlists:app` and verify it binds `127.0.0.1:8000`, and that a test with `page.goto("http://localhost:8000")` shows `ERR_CONNECTION_REFUSED` with no server and passes with the server up
- [x] 1.4 Read `tests/uv_harness_demo/` and verify how the harness runs a long-lived background command (the dev server) and records its output

## 2. Rewrite the chapter text

- [x] 2.1 Rewrite "Obey the Testing Goat" in `chapter_01.asciidoc`: uv project setup, `uv add`, Playwright install, the first FT in `tests/functional/`, the expected connection-refused failure, and drop the Firefox popup aside; verify with a text search that `pip`, `venv`, `django`, `selenium`, `geckodriver` and `manage.py` do not appear
- [x] 2.2 Rewrite "Getting Django Up and Running" as getting Quart up and running: minimal `src/superlists/__init__.py`, a one-sentence `async def` explanation, Hypercorn in a second terminal, and the FT passing; verify the listings are replayed by the chapter test (new chapters do not use `(chNNlNNN)` IDs, per `docs/porting-guide.md`)
- [x] 2.3 Rewrite "Starting a Git Repository" with the uv-made `.gitignore` and no `git init` (settled in 1.2); verify the first commit excludes `.venv/` and caches
- [x] 2.4 Update screenshots and the chapter summary/cross-references that mention Django or Firefox, and verify `make chapter_01.html` still builds without warnings

## 3. Chapter test and snapshot

- [x] 3.1 Rewrite `tests/test_chapter_01.py` as a `UvChapterTest` subclass with `previous_chapter = None`, running the server as a background process, and verify it passes with `uv run pytest tests/test_chapter_01.py`
- [x] 3.2 Create `source/chapter_01/` as plain files (no `.venv`, caches), and verify the chapter test's final snapshot diff is empty
- [x] 3.3 Alter one listing in the chapter text without touching the snapshot and verify the chapter test fails; then revert it
- [x] 3.4 Remove the chapter-1 entry from `.gitmodules` and the index, and verify `git submodule status` no longer lists it and a fresh clone has `source/chapter_01/` populated
- [x] 3.5 Verify the snapshot itself works: in a copy of it, `uv sync`, `uv run playwright install chromium`, start Hypercorn, and `uv run pytest tests/functional` passes

## 4. Repository wiring

- [x] 4.1 Update the Makefile `test_chapter_01` target and the CI matrix entry to run the new test with `uv run playwright install --with-deps chromium`, and verify the workflow file is valid YAML and other chapters' entries are unchanged
- [x] 4.2 Run the Django-era chapter 2 test setup (or at least its collection) and verify it is unaffected by this change

## 5. Review handover

- [x] 5.1 Write review notes (uv version, removed Firefox aside, any deviations from the original) and verify they sit with the built `chapter_01.html`
- [x] 5.2 Run `openspec validate port-chapter-01` and verify it reports the change as valid
- [ ] 5.3 Hand the built HTML and green test result to the maintainer for reading and approval; do not start chapter 2 until approved
