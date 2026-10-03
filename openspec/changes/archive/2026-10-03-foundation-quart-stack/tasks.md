## 1. Prototype the stack

- [x] 1.1 Create a scratch uv project with `uv init --package superlists` on Python 3.14, and verify `uv run python --version` reports 3.14
- [x] 1.2 Add Quart, Hypercorn, SQLAlchemy, aiosqlite, pytest, pytest-asyncio and pytest-playwright with `uv add`, and verify `uv sync` succeeds from a clean checkout
- [x] 1.3 Write a minimal Quart app with a home page, and verify it serves over HTTP when started with `uv run hypercorn`
- [x] 1.4 Install Chromium with `uv run playwright install chromium`, and verify a trivial headless test can open a page
- [x] 1.5 Verify Chromium runs headless without extra system setup beyond `uv run playwright install --with-deps chromium`, and note any CI install caveats in `design.md`

## 2. Shared test fixtures

- [x] 2.1 Write the live-server fixture that starts Hypercorn on a free port in a background thread, and verify a test can fetch the home page through it
- [x] 2.2 Verify the fixture stops the server after the test session and leaves no process or port in use
- [x] 2.3 Configure `pytest-asyncio` in `pyproject.toml` and verify an async unit test in `tests/unit/` using Quart's test client passes with `uv run pytest tests/unit`
- [x] 2.4 Write one functional test that opens the live-server URL with Playwright and checks the page title, in `tests/functional/`, and verify it passes headless with `uv run pytest tests/functional`

## 3. Chapter verification harness

- [x] 3.1 Read the existing `tests/` harness (the chapter test base class, the listing-ID parser and the source-repo helpers) and list which parts are Django- or Selenium-specific, delivered as notes in `design.md`
- [x] 3.2 Adapt the harness so a chapter test can replay `uv` commands and listings in a clean temporary directory, and verify it with a throwaway chapter text that has two listings
- [x] 3.3 Verify the harness fails when a listing in the text is altered without updating the checked code

## 4. Repository structure

- [x] 4.1 Create the `source/` snapshot convention for plain directories, with no submodules, and verify `git submodule status` reports nothing for a new snapshot
- [x] 4.2 Verify the existing `%.html` Makefile rule (`make chapter_NN.html`) builds one chapter's HTML, so no new target is needed, and that the page opens in a browser
- [x] 4.3 Check that the existing CI workflow's explicit chapter matrix lets ported chapters be switched over one at a time, and verify the existing harness tests still pass unchanged

## 5. Project context and handover

- [x] 5.1 Fill in `openspec/config.yaml` with the stack, conventions and verification rules, and verify `openspec status` still works
- [x] 5.2 Write a short `docs/porting-guide.md` describing the per-chapter loop (draft, run, snapshot, build, review), and verify it matches the specs
- [x] 5.3 Run `openspec validate foundation-quart-stack` and verify it reports the change as valid
- [x] 5.4 Create the `port-chapter-01` change from the conventions here, and verify its proposal references this change
