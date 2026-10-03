# Chapter snapshots

`source/chapter_NN_<name>/` holds the tutorial app (`superlists`) exactly as it
should look at the **end** of that chapter. The project root is the snapshot
directory itself: `pyproject.toml`, `src/`, `tests/` and so on sit directly
inside it.

Rules:

- Snapshots are plain directories committed to this repository. **No git
  submodules.** `git submodule status` must not list any new snapshot.
- Do not commit `.venv`, `__pycache__` or caches (already git-ignored).
  `uv.lock` is committed, but the chapter tests ignore it when diffing.
- A chapter's test starts from a plain copy of the previous chapter's snapshot,
  replays the chapter's listings and commands, and then diffs the result
  against this chapter's snapshot (see `tests/uv_chapter_test.py`).
- The old Django-edition snapshots are git submodules pointing at the upstream
  `book-example` repository. When a chapter is ported, its submodule entry is
  removed (`git rm`, and the section in `.gitmodules`) and replaced by a plain
  directory of the same name.
- `_foundation/` is the prototype of the new stack (uv, Quart, Hypercorn,
  pytest, Playwright). It is a reference for chapter 1, not a chapter snapshot.

Test layout inside a snapshot: `tests/unit/` (async, run with
`uv run pytest tests/unit`) and `tests/functional/` (Playwright against a live
server, run with `uv run pytest tests/functional`). They run as separate pytest
invocations.
