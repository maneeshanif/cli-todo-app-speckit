# Constitution Prompt for Retro Todo CLI

> **Usage:** Copy the content below and run `/sp.constitution` in Claude Code or use this file directly.

---

## Input for `/sp.constitution`

```text
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
```

---

## Expected Output

After running `/sp.constitution` with the above input, the agent will:

1. Update `.specify/memory/constitution.md` with filled placeholders
2. Validate consistency across templates
3. Generate a Sync Impact Report
4. Suggest a commit message

---

## Quick Copy Version

For fast use, copy just this:

```
Retro Todo CLI constitution with 6 principles: Retro-First UI (Rich/Textual/PyFiglet), UV Package Manager Only, TDD with pytest, Pydantic v2 Models, TinyDB Persistence, Questionary UX. Developer: maneeshanif. Stack: typer, rich, textual, pydantic, tinydb, questionary, pyfiglet, python-dateutil. Must show "Developer by: maneeshanif" in splash.
```
