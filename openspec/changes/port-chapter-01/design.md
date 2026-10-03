## Context

See `proposal.md` for why chapter 1 goes first, and `specs/chapter-01-first-test-and-server/spec.md` for the behaviour it must deliver. The shared conventions (uv-only, `src/superlists/` layout, pytest + pytest-playwright, Chromium, plain-directory snapshots) come from the archived `foundation-quart-stack` change.

Current state:
- `chapter_01.asciidoc` (514 lines) has three parts: "Obey the Testing Goat" (first FT with Selenium/Firefox, plus a Firefox-upgrade-popup aside), "Getting Django Up and Running", and "Starting a Git Repository".
- `tests/test_chapter_01.py` subclasses the Django-era `ChapterTest`, uses `update_sources_for_chapter` (submodules) and a `git remote add repo` step.
- `tests/uv_chapter_test.py` (`UvChapterTest`) already exists, with a demo in `tests/uv_harness_demo/`. `source/_foundation/superlists/` holds a verified scratch project (Quart app, live-server fixture, smoke tests) that can seed the listings.
- The fully-fledged live-server fixture exists in the foundation scratch project but is meant to be introduced later in the book, not in chapter 1.

## Goals / Non-Goals

**Goals:**
- A chapter a reader can follow with only uv and Chromium installed, with the same teaching arc as the original.
- A chapter test that proves every listing and command, including the "fails, then passes" sequence.

**Non-Goals:**
- Introducing the live-server fixture, unit tests, `async` explanations beyond one sentence, or templates. Those belong to later chapters.
- Porting the Firefox-upgrade-popup aside's content to Chromium. It has no equivalent and is dropped (noted in the review notes, per the book-conventions spec).

## Decisions

### The first FT reaches the app at a fixed address, with the server in a second terminal
This is the original book's approach (`runserver` in one terminal, FT in another) and it needs no fixture. The reader starts Hypercorn with `uv run hypercorn superlists:app` (default bind `127.0.0.1:8000`; chapter text uses `http://localhost:8000`) and the FT calls `page.goto("http://localhost:8000")`. Chapter 2 or later introduces the live-server fixture as the fix for "I have to remember to start the server".
*Alternatives:* introduce the live-server fixture now (too much machinery for page one, and hides the "nothing is listening" failure that the chapter wants the reader to see); have the test spawn the server itself (same problem).

### The FT is a pytest test using the `page` fixture, not a standalone script
The original is a plain script run with `python functional_tests.py`. Here the first FT is `tests/functional/test_first_visit.py` (a function `test_can_visit_the_site(page: Page)`; the name is short enough that pytest's `FAILED ...` line stays under the harness's 79-column wrap), run with `uv run pytest tests/functional`. That matches the layout and test-stack conventions and avoids teaching a script that is thrown away. The cost is that the reader meets pytest in chapter 1; the chapter explains it in one short aside.
*Alternative:* raw `sync_playwright()` script in the project root. Closer to the original but contradicts the spec'd layout and would be rewritten in chapter 2.

### Expected first failure is a connection error
With nothing listening, Chromium reports `net::ERR_CONNECTION_REFUSED` from `page.goto`. The chapter shows that as the "expected failure", then adds a title assertion (`"To-Do"` in `page.title()`) and a deliberate `fail("Finish the test!")`-style closing line, mirroring the original's progression. The test checks the title text; its exact value is "To-Do lists", matching the foundation scratch project.

### Project setup sequence
`uv init --lib --python 3.14 superlists` (`--lib` gives the `src/superlists/` layout without a stale `[project.scripts]` entry; `--python 3.14` is needed because uv's default is 3.12). The chapter test runs in a temp directory outside the repo, so `--no-workspace` is not needed. Then `uv add quart hypercorn` and `uv add --dev pytest pytest-playwright`, then `uv run playwright install chromium`. The chapter gives these as visible commands the test replays verbatim.
*Alternative:* adding all dev dependencies in one block up front. Rejected: dependencies are added when first needed, as the book does with Django.

### Minimal app is one module with one async view
`src/superlists/__init__.py` defines `app = Quart(__name__)` and a `home_page` view returning a tiny HTML document with the title. One sentence explains `async def`, following the foundation's risk mitigation. No templates, no blueprints.

### Git section: uv has already run `git init`
The chapter shows `cat .gitignore` (uv's already covers `.venv` and `__pycache__`), `git add .`, `git status` and `git commit`. The original's "oops, `.pyc` files" detour disappears because uv's `.gitignore` handles it, and `.pytest_cache` ignores itself.

### Snapshot and test wiring
- `source/chapter_01/` (the project root itself, as `UvChapterTest` and the porting guide expect) is a plain directory copy of the finished project, without `.venv` and caches (`uv.lock` is kept in the snapshot but excluded from the diff, as in `UvChapterTest`). The submodule entry is removed from `.gitmodules` and from the index.
- `tests/test_chapter_01.py` subclasses `UvChapterTest` with `previous_chapter = None`, replays the listings, and takes the "start server, run FT" steps from the text. Commands that start a long-running server use the harness's existing background-process support (verified against `tests/uv_harness_demo/` when implementing).
- Chapter HTML is built with `asciidoctor`, which is not installed on this machine. Installing it (Ruby gem) is a prerequisite task.

### CI and Makefile
Only the chapter-1 entry changes: install Chromium (`uv run playwright install --with-deps chromium`) and run the new test. Other entries are left alone, per the foundation's "port CI last" mitigation.

## Risks / Trade-offs

- [Port 8000 may be in use on the reader's or CI machine] → The chapter names the port, and says what to do if it is busy; the chapter test picks the default port and fails loudly with the bind error rather than guessing.
- [Server in a second terminal is awkward for the chapter test] → Run Hypercorn as a background subprocess inside the test, wait for the port, and kill it afterwards.
- [`uv init` behaviour (git init, `.gitignore`, `README`, `main.py` vs `--package`) may differ across uv versions] → Pin the commands shown in the chapter to what the installed uv produces, record the uv version in the review notes, and compare against the snapshot.
- [Reader meets pytest and async in chapter 1] → Keep to one short explanation each, and do not use fixtures beyond `page`.
- [Playwright browser download is large] → One-time `playwright install chromium`; the chapter warns about the download size.
- [Dropping the Firefox popup aside shortens the chapter] → Acceptable; record the removal in the review notes.

## Migration Plan

Port in this order: text and test together, snapshot, then Makefile/CI/`.gitmodules`. Rollback is `git revert` of the single chapter-1 commit; no other chapter depends on it until chapter 2 is ported.

## Findings from the prerequisite checks (tasks 1.1-1.4)

- uv 0.12.5, asciidoctor 2.0.26. `make chapter_01.html` builds the current chapter.
- `uv init --package superlists` defaults to Python 3.12 (`.python-version` and `requires-python = ">=3.12"`). The chapter therefore uses `uv init --package --python 3.14 superlists`, to match the stack stated in the specs.
- `uv init` creates a git repository (no commits yet), a `.gitignore` already covering `__pycache__/`, `*.py[oc]` and `.venv`, an empty `README.md`, `.python-version`, `pyproject.toml` and `src/superlists/__init__.py` (with a `main()` stub). `uv.lock` appears after the first `uv add`. So the git section does not need `git init` or most of the `.gitignore` work; it only needs `.pytest_cache/` added (to be confirmed against a real run).
- `uv run hypercorn superlists:app` binds `127.0.0.1:8000`. With nothing listening the FT fails with `net::ERR_CONNECTION_REFUSED`; with the server up it passes, using `http://localhost:8000`.
- The Django-era harness only avoids hanging on a server command when the command contains `runserver` (`SourceTree.run_command`), and `Command.type` classifies anything else starting `uv run ...` as "other command". The chapter test therefore starts and stops Hypercorn itself with `subprocess.Popen` rather than through `run_command`, and pre-handles the server listing. `SourceTree` and `ChapterTest` are not edited.


## Test harness notes (task 3.1)

The chapter test creates the project in place (`uv init ... --name superlists .`, with `cd superlists` skipped) because each harness command runs in the temp dir. It starts Hypercorn itself, because only `runserver` commands are left running by `SourceTree.run_command`. The final diff ignores `name =` lines (author details from git config) and `>=` lines (dependency lower bounds drift over time); `uv.lock` is already excluded.

The Chromium CI step runs `uvx playwright install-deps chromium` for the chapter-1 matrix entry only (`--dry-run` verified locally; not exercised on a real runner).
