# Porting guide: one chapter at a time

The book is being ported chapter by chapter to Python 3.14, Quart, SQLAlchemy,
Hypercorn, Playwright, uv and HTMX. This is the loop for one chapter. The rules
behind it live in `openspec/changes/foundation-quart-stack/` (specs and design).

## The loop

1. **Draft.** Rewrite `chapter_NN_*.asciidoc` for the new stack. Keep the
   original structure and voice. Replace anything that depended on a removed
   Django feature.
2. **Run it for real.** Execute every command and listing in a scratch
   directory, using only uv (`uv init`, `uv add`, `uv run`). Do not use pip,
   `python -m venv` or `requirements.txt`.
3. **Snapshot.** Save the end state of the project as the plain directory
   `source/chapter_NN_<name>/` (no submodules; see `source/README.md`).
4. **Test.** Write `tests/test_chapter_NN_*.py` as a subclass of
   `UvChapterTest` (`tests/uv_chapter_test.py`). It copies the previous
   snapshot, replays the chapter's listings, commands and outputs, and diffs the
   result against this chapter's snapshot. Run it with the chapter's test.
5. **Build.** `make chapter_NN_<name>.html` builds the page (needs
   `asciidoctor`). Open it in a browser to read it.
6. **Review.** The maintainer reads the page and runs the code. A chapter is
   done only when its test is green and the maintainer approves.

## Conventions to remember

- **Layout:** `src/superlists/` for code, `tests/` for tests, `pyproject.toml`
  at the project root. The snapshot directory is the project root.
- **Two test commands:** `uv run pytest tests/unit` (async, Quart test client)
  and `uv run pytest tests/functional` (Playwright, live Hypercorn server).
  They cannot run in one process, because sync Playwright leaves an event loop
  running. A bare `uv run pytest` runs only the unit tests.
- **Browser:** Chromium (`uv run playwright install chromium`; on CI use
  `--with-deps`).
- **Front end:** Jinja templates and HTMX, with Bootstrap 5.3 vendored. No Node
  on the main path.
- **Listings in chapter text:** use plain titled listings. The old
  `(chNNlNNN)` git-ref listings need the submodule history, so the new chapters
  use the text itself and let the final snapshot diff catch drift.

## Gotchas

- Never run `uv init` inside this repository without `--no-workspace`. The old
  root `pyproject.toml` would adopt the new project as a workspace member and
  create a root `uv.lock` and `.venv`.
- Building a chapter regenerates the tracked file `pygments-default.css`, and a
  newer Pygments changes colour shorthand in it. Restore it with
  `git checkout pygments-default.css` before committing.
- Do not edit the Django-era `ChapterTest` in `tests/book_tester.py`. The
  unported chapters still use it.
- To prototype, `source/_foundation/superlists` is a working reference of the
  stack, with the live-server fixture.
