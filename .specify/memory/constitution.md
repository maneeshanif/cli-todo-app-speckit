<!--
SYNC IMPACT REPORT
==================
Version change: INITIAL → 1.0.0
Modified principles: N/A (Initial creation)
Added sections:
  - I. Retro-First UI Design (NON-NEGOTIABLE)
  - II. UV Package Manager Only (NON-NEGOTIABLE)
  - III. Test-Driven Development (NON-NEGOTIABLE)
  - IV. Pydantic v2 Data Models
  - V. TinyDB Persistence
  - VI. Interactive UX with Questionary
  - Technology Stack (MANDATORY)
  - Architecture Layers
Removed sections: N/A
Templates status:
  - ✅ .specify/templates/plan-template.md (verified)
  - ✅ .specify/templates/spec-template.md (verified)
  - ✅ .specify/templates/tasks-template.md (verified)
Follow-up TODOs: None
-->

# Retro Todo CLI Constitution

## Core Principles

### I. Retro-First UI Design (NON-NEGOTIABLE)

Every interface element MUST evoke retro gaming/terminal aesthetics to create an immersive user experience:

- Use Rich library for vibrant colors, panels, tables, and progress bars
- Use PyFiglet for ASCII art banners and splash screens
- Use Textual for multi-page TUI with game-like navigation
- Color palette MUST follow cyberpunk theme: Cyan (#00FFFF), Magenta (#FF00FF), Green (#00FF00), Yellow (#FFFF00)
- All outputs MUST include visual flair - no plain text responses allowed
- Splash screen MUST display "Developer by: maneeshanif" prominently

**Rationale**: Visual excellence differentiates this application from standard CLI tools and creates memorable user experience.

### II. UV Package Manager Only (NON-NEGOTIABLE)

ALL dependency operations MUST use `uv` package manager - pip usage is forbidden:

- Package management: `uv init`, `uv add`, `uv sync`, `uv run`
- Lock files (uv.lock) MUST be committed to ensure reproducibility
- Dev dependencies MUST be separated using `--dev` flag
- No pip, pipenv, poetry, or other package managers permitted

**Rationale**: uv provides faster, more reliable dependency resolution and consistent environments across development and production.

### III. Test-Driven Development (NON-NEGOTIABLE)

TDD is mandatory for all features with strict Red-Green-Refactor cycle:

- Write tests first → Tests MUST fail (RED) → Implement code (GREEN) → Refactor
- Minimum 80% code coverage required (enforced by pytest-cov)
- Use pytest as testing framework
- Every feature implementation MUST start with a failing test
- No code merges without passing tests and coverage verification

**Rationale**: TDD ensures code correctness, prevents regressions, and produces maintainable, well-designed code.

### IV. Pydantic v2 Data Models

ALL data structures MUST use Pydantic v2 models with strict validation:

- Use Pydantic v2 syntax exclusively: `field_validator`, `model_validator` (not v1 syntax)
- Strict type hints required on all model fields
- TodoTask model serves as canonical data structure
- Validation rules enforce business constraints at data layer

**Rationale**: Pydantic v2 provides runtime type safety, automatic validation, and clear data contracts.

### V. TinyDB Persistence

JSON-based persistence using TinyDB with performance optimization:

- TinyDB as exclusive database solution for Phase I
- CachingMiddleware MUST be configured for performance
- Atomic ID generation to prevent collisions
- Clean architectural separation: models → database → services → ui

**Rationale**: TinyDB provides simple, file-based persistence without external dependencies, ideal for Phase I requirements.

### VI. Interactive UX with Questionary

ALL user inputs MUST go through Questionary for consistent, beautiful interactions:

- Custom retro styling applied to all prompts
- Confirmations required before all destructive actions (delete, overwrite)
- Beautiful select menus with icons and visual indicators
- Never use raw input() - always use Questionary

**Rationale**: Questionary provides rich, interactive prompts that match the retro aesthetic and improve user experience.

## Technology Stack (MANDATORY)

The following libraries are required and MUST be used as specified:

| Category | Library | Version | Purpose |
|----------|---------|---------|---------|
| CLI Framework | typer[all] | 0.9+ | Command-line interface with rich help |
| Terminal UI | rich | 13.0+ | Tables, panels, progress, colors |
| TUI Framework | textual | 0.40+ | Multi-page application screens |
| Data Models | pydantic | 2.0+ | Type-safe task models |
| Database | tinydb | 4.8+ | JSON document storage |
| Prompts | questionary | 2.0+ | Interactive user input |
| ASCII Art | pyfiglet | 0.8+ | Retro splash screens |
| Dates | python-dateutil | 2.8+ | Date parsing and formatting |
| Testing | pytest | 8.0+ | Test framework |
| Coverage | pytest-cov | 4.0+ | Coverage reporting |

**Package Manager**: All installations MUST use `uv add <package>` or `uv add --dev <package>`

## Architecture Layers

The application MUST follow this four-layer architecture:

### 1. Models Layer (`retro_todo/models/`)
- Pydantic v2 models: TodoTask, Priority enum, Status enum, RecurrencePattern enum
- Validation rules and business constraints
- No business logic - pure data structures

### 2. Database Layer (`retro_todo/database/`)
- TinyDB wrapper class with CachingMiddleware
- Atomic ID generation logic
- Query helper methods
- No business rules - pure persistence

### 3. Services Layer (`retro_todo/services/`)
- Business logic: CRUD operations, search, filter, sort
- Recurring task generation and handling
- Reminder detection and notification logic
- Orchestrates between database and UI layers

### 4. UI Layer (`retro_todo/ui/`)
- Splash screen with PyFiglet ASCII art
- Rich table renderers for task lists
- Questionary prompt forms for user input
- Textual TUI screens for multi-page navigation
- Theme configuration (colors, styles)

## Development Workflow

### Code Review Requirements
- All code MUST comply with principles I-VI
- Test coverage MUST meet 80% threshold
- No pip usage permitted - verify uv.lock changes only
- Visual elements MUST match cyberpunk color theme

### Testing Gates
- Unit tests for models (validation)
- Integration tests for services (business logic)
- CLI tests for command execution
- Coverage report MUST show ≥80%

### Quality Standards
- Type hints required on all functions and methods
- Docstrings required for public APIs
- No TODO comments in main branch - create issues instead
- Follow PEP 8 style guide

## Governance

- This constitution supersedes all other development practices and decisions
- Amendments require documentation via ADR (Architecture Decision Record) and approval
- All PRs MUST verify compliance with the six core principles
- Breaking a NON-NEGOTIABLE principle requires explicit justification and maintainer approval
- Version changes follow semantic versioning (MAJOR.MINOR.PATCH)
- Developer credit "Developer by: maneeshanif" MUST appear in splash screen

**Version**: 1.0.0 | **Ratified**: 2025-12-07 | **Last Amended**: 2025-12-07
