## Purpose

Defines what chapter 1 of the ported book teaches and delivers: a first failing functional test, a running Quart app served by Hypercorn, and a first git repository, backed by a verified snapshot.

## ADDED Requirements

### Requirement: Chapter keeps its three-part structure
Chapter 1 SHALL keep the original chapter's order: write a functional test first and see it fail, then get the app running so the test passes, then start a git repository and commit.

#### Scenario: Reader follows the chapter
- **WHEN** a reader reads the chapter from start to end
- **THEN** they see a failing functional test before any app code exists, a passing test after the app runs, and a first git commit last

### Requirement: First functional test fails for the right reason
The chapter SHALL have the reader write a Playwright functional test in Chromium that opens the app's home page and checks the page title, and SHALL show it failing because no server is responding.

#### Scenario: Test run with no server
- **WHEN** the reader runs the functional test before starting any server
- **THEN** it fails with a connection error, and the chapter shows that failure

#### Scenario: Test reaches the app before a live-server fixture exists
- **WHEN** the reader starts the dev server in one terminal and runs the functional test in another
- **THEN** the test reaches the app at its documented local address without relying on a live-server fixture introduced in a later chapter

### Requirement: Project is created and run with uv only
The chapter SHALL have the reader create the project with `uv init`, add `quart` and `hypercorn` with `uv add`, and run the app and tests with `uv run`. It MUST NOT mention `pip`, virtualenvs or Django.

#### Scenario: Reader sets up the project
- **WHEN** the reader follows the setup steps
- **THEN** a uv-managed project with `pyproject.toml` and a lock file exists, with `quart` and `hypercorn` recorded as dependencies

#### Scenario: Chapter text is searched for old tooling
- **WHEN** the chapter text is searched for `pip`, `venv`, `django` or `manage.py`
- **THEN** no instruction to use them is found

### Requirement: Minimal app serves a home page
The chapter SHALL have the reader create a minimal Quart app whose home page responds over HTTP on localhost, served by Hypercorn, and SHALL show the functional test then passing.

#### Scenario: Server started
- **WHEN** the reader runs the documented dev-server command
- **THEN** the home page is reachable in a browser at the stated local address

#### Scenario: Test passes against the running app
- **WHEN** the reader runs the functional test while the server is running
- **THEN** the test passes

### Requirement: Chapter ends with a git repository
The chapter SHALL have the reader initialise a git repository for the project, ignore generated files, and make a first commit.

#### Scenario: Reader commits
- **WHEN** the reader finishes the chapter
- **THEN** the project is a git repository with one commit that excludes the virtual environment and caches

### Requirement: Chapter has a verifying test and plain-directory snapshot
The chapter SHALL have `tests/test_chapter_01.py`, built on the uv chapter harness, that replays its listings and commands, and a snapshot at `source/chapter_01/` stored as plain files. The old chapter-1 submodule entry MUST be removed.

#### Scenario: Chapter test passes
- **WHEN** the chapter test is run
- **THEN** it passes only if every listing applies and each command succeeds or fails as the text states

#### Scenario: Snapshot present after clone
- **WHEN** a reader clones the repository
- **THEN** `source/chapter_01/` contains the project files without submodule initialisation

#### Scenario: Other chapters unaffected
- **WHEN** the chapter 2 test is run after this change
- **THEN** it still uses the Django-era harness and behaves as before

### Requirement: CI runs the new chapter test
The repository's CI configuration SHALL run the new chapter-1 test, with Chromium installed.

#### Scenario: CI runs chapter 1
- **WHEN** CI executes the chapter-1 entry
- **THEN** it runs the new test headless and reports its result
