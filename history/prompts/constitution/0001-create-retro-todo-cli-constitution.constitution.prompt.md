---
id: 0001
title: Create Retro Todo CLI Constitution
stage: constitution
date: 2025-12-07
surface: agent
model: claude-sonnet-4.5
feature: none
branch: main
user: maneeshanif
command: /sp.constitution
labels: ["constitution", "setup", "principles", "retro-todo-cli"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - .specify/memory/constitution.md
tests:
 - N/A (documentation)
---

## Prompt

Create a constitution for "Retro Todo CLI" - a mind-blowing retro terminal todo application.

PROJECT_NAME: Retro Todo CLI
DEVELOPER: maneeshanif
RATIFICATION_DATE: 2025-12-07

## Core Principles (6 Principles)

### I. Retro-First UI Design (NON-NEGOTIABLE)
Every interface element MUST evoke retro gaming/terminal aesthetics:
- Use Rich for vibrant colors, panels, tables, and progress bars
- Use PyFiglet for ASCII art banners and splash screens  
- Use Textual for multi-page TUI with game-like navigation
- Color palette: Cyan (#00FFFF), Magenta (#FF00FF), Green (#00FF00), Yellow (#FFFF00)
- All outputs MUST include visual flair - no plain text responses
- Splash screen MUST display "Developer by: maneeshanif" prominently

### II. UV Package Manager Only (NON-NEGOTIABLE)
- ALL dependency operations use `uv` - NEVER pip
- Commands: `uv init`, `uv add`, `uv sync`, `uv run`
- Lock files MUST be committed
- Dev dependencies separated with `--dev` flag

### III. Test-Driven Development (NON-NEGOTIABLE)
- TDD mandatory: Write tests → Tests fail (RED) → Implement (GREEN) → Refactor
- Minimum 80% code coverage required
- Use pytest with pytest-cov
- Every feature starts with a failing test

### IV. Pydantic v2 Data Models
- ALL data structures use Pydantic v2 models
- Use new v2 syntax: `field_validator`, `model_validator`
- Strict type hints with validation
- TodoTask model as canonical data structure

### V. TinyDB Persistence
- JSON storage with TinyDB
- CachingMiddleware for performance
- Atomic ID generation
- Clean separation: models → database → services → ui

### VI. Interactive UX with Questionary
- ALL user inputs go through Questionary prompts
- Custom retro styling for prompts
- Confirmations before destructive actions
- Beautiful select menus with icons

## Technology Stack (MANDATORY)

| Category | Library | Purpose |
|----------|---------|---------|
| CLI Framework | typer[all] | Command-line interface with rich help |
| Terminal UI | rich | Tables, panels, progress, colors |
| TUI Framework | textual | Multi-page application screens |
| Data Models | pydantic | Type-safe task models |
| Database | tinydb | JSON document storage |
| Prompts | questionary | Interactive user input |
| ASCII Art | pyfiglet | Retro splash screens |
| Dates | python-dateutil | Date parsing and formatting |
| Testing | pytest, pytest-cov | Test framework with coverage |

## Architecture Layers

1. **Models Layer** (`retro_todo/models/`)
   - Pydantic models: TodoTask, Priority, Status
   - Validation rules and business constraints

2. **Database Layer** (`retro_todo/database/`)
   - TinyDB wrapper with ID generation
   - Query helpers and caching

3. **Services Layer** (`retro_todo/services/`)
   - Business logic: CRUD, search, filter, sort
   - Recurring task handling, reminders

4. **UI Layer** (`retro_todo/ui/`)
   - Splash screen with PyFiglet
   - Rich tables and panels
   - Questionary prompts
   - Textual TUI screens

## Success Criteria

- [ ] Splash screen shows "Developer by: maneeshanif"
- [ ] All 10 features from Phase I implemented
- [ ] Retro cyberpunk visual theme throughout
- [ ] TinyDB persistence working
- [ ] Tests passing with >80% coverage
- [ ] Zero pip usage - uv only

## Governance

- Constitution supersedes all other practices
- Amendments require documentation and approval
- All PRs must verify compliance with principles
- Version: 1.0.0

## Response snapshot

Successfully created Retro Todo CLI Constitution v1.0.0 with 6 core principles:

1. **Retro-First UI Design (NON-NEGOTIABLE)** - Rich, PyFiglet, Textual with cyberpunk colors
2. **UV Package Manager Only (NON-NEGOTIABLE)** - Exclusive use of uv, no pip
3. **Test-Driven Development (NON-NEGOTIABLE)** - Mandatory TDD with 80% coverage
4. **Pydantic v2 Data Models** - Type-safe models with v2 syntax
5. **TinyDB Persistence** - JSON storage with CachingMiddleware
6. **Interactive UX with Questionary** - Custom retro-styled prompts

Added sections:
- Technology Stack (MANDATORY) - 9 required libraries
- Architecture Layers - 4-layer design (models/database/services/ui)
- Development Workflow - Review, testing gates, quality standards
- Governance - Amendment process and compliance requirements

Constitution file: `.specify/memory/constitution.md`
Version: 1.0.0 | Ratified: 2025-12-07

## Outcome

- ✅ Impact: Established foundational principles for Retro Todo CLI development
- 🧪 Tests: N/A (documentation artifact)
- 📁 Files: Created/Updated .specify/memory/constitution.md
- 🔁 Next prompts: /sp.specify to create feature specification
- 🧠 Reflection: Constitution provides clear constraints (uv only, TDD, 80% coverage) and technical direction (Rich/Textual/PyFiglet stack) for building retro aesthetic terminal application

## Evaluation notes (flywheel)

- Failure modes observed: None - constitution successfully created with all placeholders filled
- Graders run and results (PASS/FAIL): PASS - All 6 principles defined, version set to 1.0.0, dates in ISO format, no bracket placeholders remaining
- Prompt variant (if applicable): standard-constitution-creation-v1
- Next experiment (smallest change to try): Run /sp.specify with feature description to generate specification document
