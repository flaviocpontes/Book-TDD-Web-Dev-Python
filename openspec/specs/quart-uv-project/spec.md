# quart-uv-project Specification

## Purpose

Defines how the tutorial app, `superlists`, is set up, run and managed, so that every chapter starts from the same uv-driven project and a reader can follow along on any supported machine.

## Requirements

### Requirement: Backend setup is done entirely with uv
The book SHALL instruct readers to create, configure and run the backend project using only `uv` commands. It MUST NOT instruct readers to use `pip`, `python -m venv`, `virtualenv` or `requirements.txt` for the tutorial app.

#### Scenario: Reader creates the project
- **WHEN** a reader follows the setup steps of the first chapter
- **THEN** the project exists as a uv-managed project with a `pyproject.toml` and a lock file, created by `uv init`

#### Scenario: Reader adds a dependency
- **WHEN** a chapter introduces a new backend library
- **THEN** the chapter instructs the reader to add it with `uv add`, and the library is recorded in `pyproject.toml`

#### Scenario: Reader runs a command
- **WHEN** a chapter shows how to run the app, a test, or a tool
- **THEN** the command is run through `uv run`

### Requirement: The app runs on the specified stack
The tutorial app SHALL run on Python 3.14, using Quart as the web framework, SQLAlchemy for persistence, Hypercorn as the application server, and Playwright for browser testing.

#### Scenario: Stack versions are stated
- **WHEN** a reader opens the prerequisites chapter
- **THEN** it states the supported Python version and names each tool in the stack

#### Scenario: Reader starts the dev server
- **WHEN** a reader runs the documented dev-server command from the project root
- **THEN** the app serves its home page over HTTP on localhost

### Requirement: Project layout is consistent across chapters
The tutorial app SHALL use the same directory layout in every chapter: application code under `src/superlists/`, tests under `tests/`, and project metadata in `pyproject.toml` at the project root.

#### Scenario: Later chapter extends the project
- **WHEN** a later chapter adds a module or a test file
- **THEN** it is placed under the same `src/superlists/` and `tests/` directories established in the first chapters, without moving earlier files unless the chapter explains the move
