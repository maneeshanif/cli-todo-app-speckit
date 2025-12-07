# ADR-0004: Four-Layer Application Architecture

- **Status:** Accepted
- **Date:** 2025-12-07
- **Feature:** 001-retro-todo-app
- **Context:** The retro todo CLI requires a maintainable architecture that separates concerns, enables testability, and supports the constitution's TDD requirements while allowing independent evolution of UI, business logic, and persistence.

<!-- Significance checklist (ALL must be true to justify this ADR)
     1) Impact: Long-term consequence for architecture/platform/security? ✅ YES - Defines entire codebase structure
     2) Alternatives: Multiple viable options considered with tradeoffs? ✅ YES - Monolithic, 3-tier, hexagonal evaluated
     3) Scope: Cross-cutting concern (not an isolated detail)? ✅ YES - All modules follow this pattern -->

## Decision

Adopt a strict four-layer architecture with unidirectional dependencies:

```
┌─────────────────────────────────────────────────────────────┐
│                     UI LAYER (retro_todo/ui/)               │
│  splash.py │ tables.py │ prompts.py │ animations.py │ app.py│
│  Theme constants, Rich rendering, Questionary forms        │
└─────────────────────────────────┬───────────────────────────┘
                                  │ calls
                                  ▼
┌─────────────────────────────────────────────────────────────┐
│               SERVICES LAYER (retro_todo/services/)         │
│  todo_service.py │ search_service.py │ sort_service.py     │
│  recurrence_service.py │ Business logic, orchestration     │
└─────────────────────────────────┬───────────────────────────┘
                                  │ calls
                                  ▼
┌─────────────────────────────────────────────────────────────┐
│               DATABASE LAYER (retro_todo/database/)         │
│  db.py │ id_generator.py │ TinyDB wrapper, CRUD primitives │
└─────────────────────────────────┬───────────────────────────┘
                                  │ uses
                                  ▼
┌─────────────────────────────────────────────────────────────┐
│               MODELS LAYER (retro_todo/models/)             │
│  todo.py │ enums.py │ Pydantic v2 schemas, validation      │
└─────────────────────────────────────────────────────────────┘
```

### Layer Responsibilities

| Layer | Location | Responsibilities | Dependencies |
|-------|----------|------------------|--------------|
| **Models** | `retro_todo/models/` | Pydantic models, enums, validation rules | None (foundational) |
| **Database** | `retro_todo/database/` | TinyDB wrapper, CRUD, ID generation | Models only |
| **Services** | `retro_todo/services/` | Business logic, search, sort, recurrence | Database, Models |
| **UI** | `retro_todo/ui/` | Rich tables, Questionary prompts, splash | Services, Models |

### Dependency Rules (STRICT)

| Rule | Description |
|------|-------------|
| **Downward only** | Upper layers may call lower layers, never reverse |
| **Skip allowed** | UI may access Models directly for display purposes |
| **No cross-layer** | Services cannot call UI, Database cannot call Services |
| **Models pure** | Models have zero external dependencies |

### Directory Structure

```text
retro_todo/
├── __init__.py              # Package init with __version__
├── main.py                  # Typer CLI entry, command routing
│
├── models/                  # LAYER 1: Data models
│   ├── __init__.py
│   ├── todo.py              # TodoTask Pydantic model
│   └── enums.py             # Priority, Status, RecurrencePattern
│
├── database/                # LAYER 2: Persistence
│   ├── __init__.py
│   ├── db.py                # TinyDB wrapper, CachingMiddleware
│   └── id_generator.py      # Atomic ID generation
│
├── services/                # LAYER 3: Business logic
│   ├── __init__.py
│   ├── todo_service.py      # CRUD operations
│   ├── search_service.py    # Text search, filtering
│   ├── sort_service.py      # Multi-field sorting
│   └── recurrence_service.py# Recurring task generation
│
└── ui/                      # LAYER 4: User interface
    ├── __init__.py
    ├── theme.py             # Cyberpunk color constants
    ├── splash.py            # PyFiglet ASCII art banner
    ├── tables.py            # Rich table rendering
    ├── prompts.py           # Questionary styled forms
    ├── animations.py        # Completion celebrations
    └── app.py               # Textual TUI (optional Phase II)
```

### Testing Strategy

Each layer has dedicated test modules maintaining the same separation:

```text
tests/
├── unit/                    # Fast, isolated tests
│   ├── test_models.py       # Model validation
│   ├── test_enums.py        # Enum constraints
│   └── test_id_generator.py # ID atomicity
│
├── integration/             # Cross-layer tests
│   ├── test_database.py     # TinyDB operations
│   ├── test_todo_service.py # Service + Database
│   ├── test_search.py       # Search correctness
│   └── test_recurrence.py   # Recurrence logic
│
└── e2e/                     # Full stack tests
    ├── test_cli_commands.py # Typer command execution
    └── test_workflows.py    # Complete user journeys
```

## Consequences

### Positive

- **Testability**: Each layer can be unit tested in isolation with mocks
- **Maintainability**: Changes in one layer don't ripple to others
- **Separation of concerns**: Clear boundaries between data, logic, and presentation
- **Team collaboration**: Different developers can work on layers independently
- **Reusability**: Services can be reused if alternative UI (web, API) added
- **TDD alignment**: Clean interfaces enable Red-Green-Refactor cycle

### Negative

- **Boilerplate**: More files and imports than monolithic approach
- **Indirection**: Simple operations traverse multiple layers
- **Learning curve**: Developers must understand layer boundaries
- **Over-engineering risk**: For simple features, architecture may feel heavy

## Alternatives Considered

### Alternative A: Monolithic single-file

- **Pros**: Simple, no imports, everything in one place
- **Cons**: Untestable, unmaintainable at scale, violates TDD principle
- **Why rejected**: Does not support 80% coverage requirement (constitution)

### Alternative B: Traditional 3-tier (MVC)

- **Pros**: Familiar pattern, widely understood
- **Cons**: Less granular than needed, model-view coupling common
- **Why rejected**: Merges models/database, loses clean validation boundary

### Alternative C: Hexagonal Architecture (Ports & Adapters)

- **Pros**: Maximum flexibility, swappable adapters
- **Cons**: Significant complexity, interface explosion, over-engineered
- **Why rejected**: Overkill for single-database, single-UI application

### Alternative D: Django-style apps

- **Pros**: Feature-based organization, familiar to Django developers
- **Cons**: Adds framework concepts, mixes concerns within "apps"
- **Why rejected**: CLI app doesn't benefit from web framework patterns

## References

- Feature Spec: [specs/001-retro-todo-app/spec.md](../../specs/001-retro-todo-app/spec.md)
- Implementation Plan: [specs/001-retro-todo-app/plan.md](../../specs/001-retro-todo-app/plan.md) (Project Structure section)
- Constitution: [.specify/memory/constitution.md](../../.specify/memory/constitution.md) (Principles III, IV, V)
- Task Breakdown: [specs/001-retro-todo-app/tasks.md](../../specs/001-retro-todo-app/tasks.md)
