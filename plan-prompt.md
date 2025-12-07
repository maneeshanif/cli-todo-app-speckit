# Plan Prompt for Retro Todo CLI

> **Usage:** Run `/sp.plan` in Claude Code after creating the specification. This file contains architecture and implementation planning guidance.

---

## Input for `/sp.plan`

```text
Plan the implementation architecture for Retro Terminal Todo Manager using the sub-agent and skills system.

## Technical Context

### Primary Technologies
| Technology | Version | Purpose |
|------------|---------|---------|
| Python | 3.11+ | Runtime |
| uv | latest | Package management (NOT pip) |
| typer | 0.9+ | CLI framework with rich support |
| rich | 13.0+ | Terminal formatting, tables, panels |
| textual | 0.40+ | Multi-page TUI framework |
| pydantic | 2.0+ | Data models with validation |
| tinydb | 4.8+ | JSON document database |
| questionary | 2.0+ | Interactive prompts |
| pyfiglet | 0.8+ | ASCII art generation |
| python-dateutil | 2.8+ | Date parsing |
| pytest | 8.0+ | Testing framework |
| pytest-cov | 4.0+ | Coverage reporting |

### Sub-Agent Delegation Plan

```
┌─────────────────────────────────────────────────────────────┐
│                    IMPLEMENTATION ORDER                      │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Phase 1: Foundation (SetupAgent)                           │
│  ├── uv init + pyproject.toml                               │
│  ├── Directory structure creation                           │
│  └── Dependency installation                                │
│                                                              │
│  Phase 2: Data Layer (DataModelAgent)                       │
│  ├── Pydantic models (TodoTask, Enums)                      │
│  ├── TinyDB wrapper with ID generation                      │
│  └── Database configuration                                 │
│                                                              │
│  Phase 3: Business Logic (FeatureAgent)                     │
│  ├── CRUD operations (TodoService)                          │
│  ├── Search and filter logic                                │
│  ├── Sort functionality                                     │
│  └── Recurring task handler                                 │
│                                                              │
│  Phase 4: User Interface (UIAgent)                          │
│  ├── Splash screen with PyFiglet                            │
│  ├── Rich table renderer                                    │
│  ├── Questionary prompt forms                               │
│  ├── Textual TUI screens                                    │
│  └── Animation effects                                      │
│                                                              │
│  Phase 5: Testing (TestAgent)                               │
│  ├── Model unit tests                                       │
│  ├── Service integration tests                              │
│  ├── CLI command tests                                      │
│  └── Coverage verification                                  │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## Project Structure

```
cli-todo-hackhaton/
├── CLAUDE.md                    # Project specification
├── pyproject.toml               # uv project config
├── uv.lock                      # Locked dependencies
├── todo_data.json               # TinyDB storage file
│
├── retro_todo/                  # Main package
│   ├── __init__.py              # Package init with version
│   ├── main.py                  # Typer CLI entry point
│   │
│   ├── models/                  # Pydantic models
│   │   ├── __init__.py
│   │   └── todo.py              # TodoTask, Priority, Status, Recurrence
│   │
│   ├── database/                # TinyDB layer
│   │   ├── __init__.py
│   │   └── db.py                # Database wrapper, ID generation
│   │
│   ├── services/                # Business logic
│   │   ├── __init__.py
│   │   └── todo_service.py      # CRUD, search, filter, recurring
│   │
│   └── ui/                      # UI components
│       ├── __init__.py
│       ├── splash.py            # PyFiglet splash screen
│       ├── tables.py            # Rich table rendering
│       ├── prompts.py           # Questionary forms
│       ├── theme.py             # Color constants
│       └── app.py               # Textual TUI (optional)
│
├── tests/                       # Test suite
│   ├── __init__.py
│   ├── conftest.py              # Pytest fixtures
│   ├── test_models.py           # Model validation tests
│   ├── test_database.py         # DB operation tests
│   ├── test_services.py         # Business logic tests
│   └── test_cli.py              # CLI command tests
│
├── .claude/                     # Sub-agents and skills
│   ├── agents/                  # Specialist agents
│   │   ├── setup-agent.md
│   │   ├── data-model-agent.md
│   │   ├── feature-agent.md
│   │   ├── ui-agent.md
│   │   └── test-agent.md
│   └── skills/                  # Reusable skills
│       ├── setup-skill/
│       ├── dependency-skill/
│       ├── model-skill/
│       ├── database-skill/
│       ├── crud-skill/
│       ├── search-skill/
│       ├── filter-skill/
│       ├── render-skill/
│       ├── prompt-skill/
│       └── animation-skill/
│
└── specs/                       # Feature specifications
    └── 1-retro-todo-app/
        ├── spec.md
        ├── plan.md
        └── tasks.md
```

## Key Design Decisions

### 1. Library Integration Strategy

**Rich + Typer Integration:**
```python
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(rich_markup_mode="rich")
console = Console()

@app.command()
def list():
    """[cyan]List all tasks[/cyan] with beautiful formatting."""
    table = Table(title="📋 Tasks", border_style="cyan")
    # ... build table
    console.print(table)
```

**Questionary Styling:**
```python
from questionary import Style

retro_style = Style([
    ('qmark', 'fg:#00ffff bold'),      # Cyan question mark
    ('question', 'fg:#ff00ff bold'),    # Magenta question
    ('answer', 'fg:#00ff00'),           # Green answer
    ('pointer', 'fg:#00ffff bold'),     # Cyan pointer
    ('highlighted', 'fg:#ff00ff bold'), # Magenta highlight
])
```

**PyFiglet Splash:**
```python
import pyfiglet
from rich.panel import Panel
from rich.text import Text

def show_splash():
    ascii_art = pyfiglet.figlet_format("TODO", font="slant")
    panel = Panel(
        Text(ascii_art, style="cyan"),
        title="🎮 RETRO TASK MANAGER",
        subtitle="Developer by: maneeshanif",
        border_style="magenta"
    )
    console.print(panel)
```

### 2. TinyDB Setup

```python
from tinydb import TinyDB
from tinydb.middlewares import CachingMiddleware
from tinydb.storages import JSONStorage

db = TinyDB(
    'todo_data.json',
    storage=CachingMiddleware(JSONStorage)
)
tasks_table = db.table('tasks')
```

### 3. Pydantic v2 Model

```python
from pydantic import BaseModel, field_validator
from datetime import datetime
from enum import Enum

class Priority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"

class TodoTask(BaseModel):
    id: int
    title: str
    priority: Priority = Priority.MEDIUM
    
    @field_validator('title')
    @classmethod
    def title_not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError('Title cannot be empty')
        return v.strip()
```

## Constitution Check

| Principle | Status | Notes |
|-----------|--------|-------|
| Retro-First UI | ✅ | Rich + Textual + PyFiglet |
| UV Only | ✅ | All deps via uv |
| TDD | ⏳ | Tests with pytest |
| Pydantic v2 | ✅ | New syntax |
| TinyDB | ✅ | CachingMiddleware |
| Questionary | ✅ | Custom retro style |

## Implementation Tasks Preview

1. **SetupAgent Tasks**
   - [ ] Run `uv init` and configure pyproject.toml
   - [ ] Create directory structure
   - [ ] Install dependencies with `uv add`

2. **DataModelAgent Tasks**
   - [ ] Create Priority, Status, RecurrencePattern enums
   - [ ] Create TodoTask Pydantic model
   - [ ] Create TinyDB wrapper class

3. **FeatureAgent Tasks**
   - [ ] Implement TodoService with CRUD
   - [ ] Add search functionality
   - [ ] Add filter functionality
   - [ ] Add sort functionality
   - [ ] Add recurring task logic

4. **UIAgent Tasks**
   - [ ] Create splash screen with PyFiglet
   - [ ] Create Rich table renderer
   - [ ] Create Questionary prompt forms
   - [ ] Apply cyberpunk color theme

5. **TestAgent Tasks**
   - [ ] Write model validation tests
   - [ ] Write service tests
   - [ ] Write CLI integration tests
   - [ ] Verify >80% coverage

## Risks and Mitigations

1. **Risk:** Textual complexity for Phase I
   - **Mitigation:** Start with Rich-only CLI, add Textual TUI as enhancement

2. **Risk:** Time constraint (due Dec 7)
   - **Mitigation:** Focus on core 10 features, polish later

3. **Risk:** Integration between libraries
   - **Mitigation:** Use proven patterns from Context7 docs
```

---

## Expected Output

After running `/sp.plan` with the above input, the agent will:

1. Read the feature spec from `specs/1-retro-todo-app/spec.md`
2. Generate `specs/1-retro-todo-app/plan.md` with architecture
3. Create Phase 0 research.md if needed
4. Generate data-model.md and contracts
5. Report all generated artifacts

---

## Quick Copy Version

For fast use, copy just this:

```
Plan Retro Todo CLI: 5 phases using sub-agents. Phase 1 SetupAgent (uv init, deps), Phase 2 DataModelAgent (Pydantic TodoTask, TinyDB), Phase 3 FeatureAgent (CRUD, search, filter, sort, recurring), Phase 4 UIAgent (PyFiglet splash, Rich tables, Questionary prompts), Phase 5 TestAgent (pytest >80% coverage). Structure: retro_todo/{models,database,services,ui}. Libraries: typer, rich, textual, pydantic, tinydb, questionary, pyfiglet.
```
