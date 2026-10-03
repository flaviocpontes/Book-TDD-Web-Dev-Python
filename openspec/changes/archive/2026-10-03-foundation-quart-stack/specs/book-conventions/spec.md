## Purpose

Fixes the front-end approach and the writing style of the ported book, so that chapters written at different times read as one coherent book.

## ADDED Requirements

### Requirement: Front end is server-rendered with HTMX
The tutorial app's pages SHALL be rendered on the server from Jinja templates, and client-side interactivity SHALL be provided by HTMX attributes. The main path of the book MUST NOT require Node.js, npm or a JavaScript bundler.

#### Scenario: Interactive behaviour is added
- **WHEN** a chapter adds dynamic page behaviour such as submitting an item without a full reload
- **THEN** it is implemented with HTMX requests that return HTML fragments from the server

#### Scenario: Reader has no Node installed
- **WHEN** a reader follows the main path of the book
- **THEN** every step can be completed without installing Node.js

### Requirement: Bootstrap is vendored
The book SHALL use Bootstrap 5.3 for styling, provided as static files in the project rather than fetched by a package manager.

#### Scenario: Styling chapter
- **WHEN** the styling chapter adds Bootstrap
- **THEN** the files are placed in the app's static directory and linked from the base template

### Requirement: Original structure and voice are kept
Each ported chapter SHALL keep the structure, section order and teaching intent of the original chapter where the new stack allows, and SHALL be written in the original author's conversational style. Content that no longer applies to the new stack MUST be replaced, not left in place.

#### Scenario: Chapter content depends on a removed Django feature
- **WHEN** an original section teaches a Django-specific feature with no equivalent in the new stack
- **THEN** the ported chapter replaces it with the closest equivalent teaching point, or removes it and says so in the review notes

### Requirement: Attribution is preserved
The published book SHALL credit the original author and book, and SHALL state that it is an adaptation under the terms agreed with the author.

#### Scenario: Reader opens the book
- **WHEN** a reader opens the title page or footer
- **THEN** the original author and the adaptation notice are visible
