## Context

The original book teaches TDD by building a to-do list app on Django. Each chapter has an `.asciidoc` file, a `tests/test_chapter_*.py` that replays its listings, and a `source/chapter_*/superlists` snapshot kept as a git submodule pointing at the upstream author's repository. See `proposal.md` for the motivation for porting to Quart.

The repository today still contains the Django-era toolchain (`pyproject.toml` with Django and Selenium, `Dockerfile`, `Makefile`, the GitHub Actions workflow). The chapters will be ported in order, so for a long time the repository will hold a mix of ported and unported chapters.

## Goals / Non-Goals

**Goals:**
- Fix the shared conventions (layout, test stack, front-end stance, snapshot storage) once, so every chapter change inherits them.
- Make the first chapter a small, safe step: a uv project, a minimal Quart app, Hypercorn, and one Playwright test.

**Non-Goals:**
- Writing any chapter text. That belongs to the per-chapter changes.
- Porting deployment (Docker, Ansible, CI). Those chapters come late and get their own changes.
- Publishing to GitHub Pages. That is a separate change, `publish-github-pages`.

## Decisions

### Project layout: `src/` layout, project named `superlists`
Application code goes in `src/superlists/`, tests in `tests/`, and metadata in `pyproject.toml`. The `src/` layout avoids tests accidentally importing the working directory instead of the installed package, and it matches what `uv init --package` creates.
*Alternative:* flat layout like Django's `manage.py` project. Rejected because it makes the package boundary less clear, and Quart has no `manage.py`-style convention to follow.

### One uv project per chapter snapshot, extended in place
Each `source/chapter_NN_*/` directory holds the full project as it stands at the end of that chapter, with its own `pyproject.toml` and `uv.lock`. A reader works in a single project of their own, and the snapshot is the reference to compare against.
*Alternative:* one shared project with git tags per chapter. Rejected because the requirement is no submodules and plain directories, and tags would hide the state from a reader browsing the repository.

### Test runner: pytest, `pytest-asyncio`, `pytest-playwright`
Quart is async, so tests are async. pytest with `pytest-asyncio` is the common choice, and `pytest-playwright` provides the browser fixtures. `asyncio_mode = "auto"` in `pyproject.toml` keeps test code free of decorators, which matters for a teaching book.
*Alternative:* `unittest.IsolatedAsyncioTestCase`, which would stay closer to the original book. Rejected because Django's test runner is gone anyway, and Playwright's pytest integration is the best-supported path.

### Unit and functional tests run as separate pytest invocations
Decided by the maintainer. A sync Playwright test leaves an event loop running in the main thread, so async tests that run after it fail with `Runner.run() cannot be called from a running event loop`. Tests are split into `tests/unit/` (async, Quart test client) and `tests/functional/` (sync Playwright, live server) and run with two commands. This is also a good fit for the book: unit tests are the fast inner loop and functional tests the slow outer loop.
*Alternatives:* `pytest-playwright-asyncio` (a single async model, but it hung with our live-server fixture in a quick trial and was not pursued), or forcing test order within one run (fragile).

### Live-server fixture runs Hypercorn in a background thread
A session-scoped fixture starts Hypercorn on a free port in a thread with its own event loop, waits until the port accepts connections, and yields the base URL. This avoids subprocess management in the early chapters and keeps tracebacks visible.
*Alternative:* a subprocess started with `uv run hypercorn`. Better isolation, but slower and harder to debug for readers. It can be introduced later, in the deployment chapters, when the book needs to test a real container.

### Database: SQLAlchemy 2 async with SQLite via `aiosqlite`
SQLite keeps the setup free of external services, matching the original book. Alembic is introduced when the book first needs a schema change. The database arrives in the chapter that introduces persistence, not in the foundation.

### Front end: Jinja + HTMX, Bootstrap 5.3 vendored, no Node
HTMX is added as a single vendored JavaScript file, like Bootstrap, so the main path stays free of a JS toolchain. If a client-side testing example is wanted, it is an optional section using Node's built-in test runner.
*Alternative:* React with TypeScript. Rejected as it would turn the book into a JavaScript book and require a second toolchain.

### Verification: reuse the existing chapter-test approach
The existing tests replay listings identified by IDs such as `(ch25l001)` in the chapter text. The new tests keep that idea, since it is what makes the book trustworthy. The tooling in `tests/` is adapted to run the new commands, not rewritten from scratch.

## Risks / Trade-offs

- [The chapter-test harness is Django- and Selenium-specific] → Inspect it during the first chapter's port and adapt only what is needed. Do not rewrite the whole harness up front.
- [Async adds a learning cost early in the book] → Introduce `async def` with a short, explicit explanation in chapter 1, and keep early examples minimal.
- [Mixed old and new chapters in the repository break the existing CI] → Port the CI matrix last, and exclude unported chapters from it as each port begins.
- [Playwright browser downloads are large and slow in CI] → Install only the one browser the tests use, and cache it.
- [Quart's ecosystem is smaller than Django's for forms and auth] → Decide those libraries in the changes for the forms and auth chapters, where the choice can be evaluated against the real code.

### Default functional-test browser: Chromium
Decided by the maintainer. Chromium is Playwright's best-supported browser, is a single install, and works headless in CI, so CI only needs to install and cache one browser.

Verified locally (Playwright 1.63): `uv run playwright install chromium` followed by a headless `pytest-playwright` test passes with no other system setup. Caveat: on a fresh Linux CI image the system libraries are usually missing, so CI should run `uv run playwright install --with-deps chromium`. That was not exercised on a CI runner during this change.

### Source format: AsciiDoc stays
Decided by the maintainer. The asciidoctor build and the chapter tests depend on it.

## Harness Notes (task 3.1)

How the existing harness in `tests/` works: each `test_chapter_NN.py` subclasses `ChapterTest` (`book_tester.py`), which parses the chapter's **built HTML** (`chapter_NN.html`, produced by asciidoctor) into an ordered list of code listings, commands and outputs (`book_parser.py`). The test walks that list, writes files, applies diffs, runs commands in a temp directory (`sourcetree.py`), and compares real output to the output shown in the book after normalising noise such as hashes, ports and timestamps. At the end it diffs the temp tree against the chapter snapshot.

Reusable as-is: the HTML listing parser, the `Output`/`Command`/`CodeListing` types, the temp-dir and command runner in `SourceTree`, the output normalisers that are not framework-specific (git hashes, callouts, ports, object ids), and the diff-checking logic in `Commit`.

Specific to Django, Selenium or the old repo layout, and so needing replacement:
- `prep_virtualenv`, which runs `uv venv` and `uv pip install django selenium`. The new stack uses `uv init`, `uv add` and `uv run`, with no manual venv.
- `prep_database`, `_manage_py`, `start_dev_server`, `restart_dev_server`, `run_unit_tests`, `run_fts` and `run_interactive_manage_py`, which all call `manage.py`.
- Normalisers for geckodriver, Firefox ESR versions, Selenium trace ids, Django `IntegrityError` text, migration timestamps and `manage.py` prompts.
- Hard-coded Bootstrap 3.3.4 download and the `gunicorn whitenoise` install.
- The **snapshot mechanism**: `update_source_repo.py` and `SourceTree.start_with_checkout` use git submodules, `git fetch`, per-chapter branches and `git diff repo/<chapter>`. With plain directories this becomes: copy the previous chapter's `source/chapter_NN/` into the temp dir to start, and compare the final temp tree against `source/chapter_NN/` with a directory diff.

Approach decided from this: do not edit `ChapterTest`, because the unported Django chapters still use it. Add a new `UvChapterTest` subclass in a new module that overrides only the points above.

Prerequisite found: the chapter HTML is built by `asciidoctor`, which is not installed on the development machine (no `ruby`/`asciidoctor`). Tasks 3.2, 3.3 and 4.2 need it.
