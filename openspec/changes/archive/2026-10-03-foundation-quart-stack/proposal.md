## Why

The book's tutorial app is built on Django, Selenium, gunicorn and pip, and its examples are showing their age. We are porting the whole book, prose and code, to a modern async Python stack (Python 3.14, Quart, SQLAlchemy, Hypercorn, Playwright, uv) with an HTMX front end. The port will be done one chapter at a time, and every chapter depends on shared conventions. Those conventions must be fixed once, before chapter 1 is written, or each chapter will have to be reworked later.

## What Changes

- Define the project layout of the tutorial app (`superlists`) and require that its entire backend setup is done with `uv` (`uv init`, `uv add`, `uv run`), with no `pip` or manual virtualenv steps.
- Define the test stack the book teaches: pytest with `pytest-asyncio` for unit and integration tests, `pytest-playwright` for functional tests, and a live-server fixture that runs Hypercorn.
- Define the front-end stance: server-rendered Jinja templates, HTMX for interactivity, Bootstrap 5.3 vendored as static files, and no Node toolchain on the main path.
- Define how chapter code snapshots are stored: plain directories under `source/chapter_NN_*/` in this repository, with **no git submodules**.
- Define how each chapter is verified: a per-chapter test that replays the chapter's commands and listings, and a green result is required before the chapter is accepted.
- Define the writing conventions for the port: keep the original author's voice and chapter structure, and rewrite the content for the new stack.
- Fill in `openspec/config.yaml` with this stack context so that later chapter changes inherit it.

## Capabilities

### New Capabilities
- `quart-uv-project`: The layout, dependency management and run commands of the `superlists` tutorial app, all driven by `uv`.
- `chapter-verification`: The pytest and Playwright test stack, the live-server fixture, and the rules that tie each chapter's text to a test and a source snapshot.
- `book-conventions`: The front-end stance, the snapshot storage rule, and the prose style rules that every ported chapter follows.

### Modified Capabilities
<!-- None: the project has no existing specs. -->

## Impact

- New files only under `openspec/` in this change. No chapter text, tutorial code or tests are written by this change's planning stage.
- When the tasks are applied, they will add a `pyproject.toml` for the tutorial app, a shared test fixture module, and the directory layout for `source/`.
- The existing Django-era `Makefile`, `pyproject.toml`, `Dockerfile`, CI workflow and `.gitmodules` are affected, and are updated as chapters are ported rather than all at once.
- The old `source/` submodules are replaced by plain directories, one chapter at a time.
