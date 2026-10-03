## Purpose

Ensures that everything a chapter tells the reader to type or run actually works, by tying each chapter to an automated test and a source snapshot that the reader can also inspect.

## ADDED Requirements

### Requirement: Each chapter has a verifying test
Every ported chapter SHALL have a corresponding test in `tests/` that replays the chapter's commands and code listings in a clean temporary directory and fails if any step does not produce the output the chapter shows.

#### Scenario: Chapter test passes
- **WHEN** the chapter's test is run against the chapter text
- **THEN** it passes only if every listing applies and every shown command succeeds or fails as the text states

#### Scenario: Text and code drift apart
- **WHEN** a listing in the chapter text is changed without updating the code it is checked against
- **THEN** the chapter test fails

### Requirement: Tests use pytest with async support
Unit and integration tests in the book SHALL use pytest with `pytest-asyncio` and Quart's async test client. Functional tests SHALL use `pytest-playwright`. Unit tests and functional tests SHALL live in separate directories, `tests/unit/` and `tests/functional/`, and SHALL be run as separate pytest invocations, because the synchronous Playwright fixtures and async tests cannot share one pytest process.

#### Scenario: Reader runs unit tests
- **WHEN** a reader runs `uv run pytest tests/unit` on the tutorial app
- **THEN** all unit and integration tests are collected and pass without starting a browser

#### Scenario: Reader runs functional tests
- **WHEN** a reader runs `uv run pytest tests/functional` on the tutorial app
- **THEN** all functional tests are collected and run in a browser against a live server

### Requirement: Functional tests run against a live server
Functional tests SHALL run against a real Hypercorn server started by a shared fixture on a free port, and SHALL be able to run headless in CI.

#### Scenario: Functional test needs the site
- **WHEN** a functional test requests the live-server fixture
- **THEN** a server is running and reachable at the fixture's URL for the duration of the test, and is stopped afterwards

#### Scenario: Browsers are installed
- **WHEN** a reader runs the documented Playwright browser-install command with `uv run`
- **THEN** the browser needed by the functional tests is available

### Requirement: A chapter is accepted only when verified and read
A chapter SHALL be considered done only when its test is green and the maintainer has read the rendered page and approved it.

#### Scenario: Chapter ready for review
- **WHEN** a chapter is delivered for review
- **THEN** its test result and a built HTML page are available for the maintainer to inspect

### Requirement: Source snapshots are plain directories
The state of the tutorial app at the end of each chapter SHALL be stored as a plain directory at `source/chapter_NN_<name>/` in this repository. Git submodules MUST NOT be used.

#### Scenario: Snapshot is checked out
- **WHEN** a reader clones the repository
- **THEN** every chapter snapshot is present without any submodule initialisation
