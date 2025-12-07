# Quickstart Guide: Retro Terminal Todo Manager

**Feature**: 001-retro-todo-app  
**Date**: 2025-12-07  
**For**: Developers joining the project

## Prerequisites

- Python 3.11 or higher
- [uv](https://github.com/astral-sh/uv) package manager installed
- Git for version control
- Terminal with ANSI color and Unicode support

### Installing uv

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Or via Homebrew (macOS)
brew install uv

# Or via pip (if you must, but we don't use pip after this!)
pip install uv
```

Verify installation:
```bash
uv --version
# Expected: uv 0.1.x or higher
```

---

## Quick Start (5 Minutes)

### 1. Clone Repository

```bash
git clone https://github.com/maneeshanif/cli-todo-app-speckit.git
cd cli-todo-app-speckit

# Switch to feature branch
git checkout 001-retro-todo-app
```

### 2. Install Dependencies

```bash
# Initialize Python environment and install all dependencies
uv sync

# This creates:
# - .venv/ directory (Python virtual environment)
# - uv.lock (locked dependency versions)
```

### 3. Run Application

```bash
# Run CLI directly
uv run python -m retro_todo.main

# Or use shortcut (if configured in pyproject.toml)
uv run retro-todo
```

You should see the retro splash screen!

### 4. Run Tests

```bash
# Run entire test suite
uv run pytest

# Run with coverage report
uv run pytest --cov=retro_todo --cov-report=term-missing

# Run specific test file
uv run pytest tests/unit/test_models.py
```

---

## Project Structure Walkthrough

```
cli-todo-hackhaton/
├── retro_todo/              # Main application package
│   ├── models/              # Pydantic data models
│   │   ├── todo.py          # TodoTask model
│   │   └── enums.py         # Priority, Status, Recurrence enums
│   ├── database/            # TinyDB persistence
│   │   ├── db.py            # Database wrapper
│   │   └── id_generator.py # ID generation
│   ├── services/            # Business logic
│   │   ├── todo_service.py  # CRUD operations
│   │   ├── search_service.py# Search/filter
│   │   └── recurrence_service.py # Recurring tasks
│   └── ui/                  # User interface
│       ├── theme.py         # Color constants
│       ├── splash.py        # Splash screen
│       ├── tables.py        # Rich tables
│       ├── prompts.py       # Questionary forms
│       └── main.py          # CLI entry point
│
├── tests/                   # Test suite
│   ├── unit/                # Unit tests (models, enums)
│   ├── integration/         # Integration tests (services, DB)
│   └── e2e/                 # End-to-end CLI tests
│
├── specs/001-retro-todo-app/# Design documents
│   ├── spec.md              # Feature specification
│   ├── plan.md              # Implementation plan
│   ├── research.md          # Technology research
│   ├── data-model.md        # Data models
│   └── contracts/           # API contracts
│
├── pyproject.toml           # Project configuration (uv)
├── uv.lock                  # Locked dependencies
└── todo_data.json           # Task database (gitignored)
```

---

## Development Workflow

### Constitution Principles (MUST Follow)

**NON-NEGOTIABLE Rules**:
1. **Retro-First UI**: Use Rich/Textual/PyFiglet, cyberpunk colors always
2. **UV Only**: NEVER use pip - all installs via `uv add`
3. **Test-Driven Development**: Write tests first (Red-Green-Refactor)
4. **Pydantic v2**: Use `@field_validator` (not v1 `@validator`)
5. **TinyDB**: JSON persistence with CachingMiddleware
6. **Questionary**: All user inputs via interactive prompts (no raw `input()`)

See `.specify/memory/constitution.md` for full details.

### Adding a New Feature

**TDD Workflow** (Red-Green-Refactor):

1. **Write failing test (RED)**:
```bash
# Create test file
touch tests/unit/test_my_feature.py

# Write test that fails
uv run pytest tests/unit/test_my_feature.py
# Expected: FAILED (test should fail - no implementation yet)
```

2. **Implement feature (GREEN)**:
```bash
# Create implementation file
touch retro_todo/services/my_feature.py

# Implement minimum code to pass test
uv run pytest tests/unit/test_my_feature.py
# Expected: PASSED (1 test)
```

3. **Refactor**:
```bash
# Clean up code, add type hints, docstrings
# Run tests to ensure still passing
uv run pytest tests/unit/test_my_feature.py
```

4. **Verify coverage**:
```bash
uv run pytest --cov=retro_todo.services.my_feature --cov-report=term-missing
# Expected: ≥80% coverage
```

### Adding Dependencies

**ALWAYS use uv** (not pip):

```bash
# Production dependency
uv add <package>

# Development dependency (tests, linting, etc.)
uv add --dev <package>

# Examples
uv add rich         # Production
uv add --dev pytest # Dev only
```

**NEVER do this**:
```bash
# ❌ FORBIDDEN - violates constitution principle II
pip install <package>
```

### Running Different Test Categories

```bash
# Unit tests only (fast, no I/O)
uv run pytest tests/unit/

# Integration tests (database, services)
uv run pytest tests/integration/

# End-to-end tests (full CLI commands)
uv run pytest tests/e2e/

# Run tests matching pattern
uv run pytest -k "test_add"

# Run with verbose output
uv run pytest -v

# Run with coverage + HTML report
uv run pytest --cov=retro_todo --cov-report=html
# Opens htmlcov/index.html in browser
```

---

## Common Tasks

### Task 1: Create a New Pydantic Model

```python
# retro_todo/models/my_model.py
from pydantic import BaseModel, Field, field_validator
from datetime import datetime

class MyModel(BaseModel):
    """My model description."""
    
    id: int
    name: str = Field(min_length=1, max_length=100)
    created_at: datetime = Field(default_factory=datetime.now)
    
    @field_validator('name')
    @classmethod
    def name_not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError('Name cannot be empty')
        return v.strip()
```

**Test it**:
```python
# tests/unit/test_my_model.py
import pytest
from retro_todo.models.my_model import MyModel

def test_name_cannot_be_empty():
    with pytest.raises(ValueError, match="Name cannot be empty"):
        MyModel(id=1, name="   ")
```

### Task 2: Add a Service Method

```python
# retro_todo/services/my_service.py
from retro_todo.database.db import tasks_table
from retro_todo.models.todo import TodoTask

class MyService:
    def get_urgent_tasks(self) -> list[TodoTask]:
        """Get all tasks with Urgent priority."""
        from retro_todo.models.enums import Priority
        
        results = tasks_table.search(
            lambda task: task['priority'] == Priority.URGENT.value
        )
        return [TodoTask.from_dict(task) for task in results]
```

**Test it**:
```python
# tests/integration/test_my_service.py
def test_get_urgent_tasks(test_db_with_tasks):
    service = MyService()
    urgent = service.get_urgent_tasks()
    
    assert all(task.priority == Priority.URGENT for task in urgent)
```

### Task 3: Add a CLI Command

```python
# retro_todo/ui/main.py
import typer
from rich.console import Console

app = typer.Typer(rich_markup_mode="rich")
console = Console()

@app.command()
def my_command(
    arg: str = typer.Argument(..., help="Required argument")
):
    """[cyan]My command description[/cyan] with Rich markup."""
    console.print(f"[green]✓[/green] Received: {arg}")
```

**Test it**:
```python
# tests/e2e/test_my_command.py
from typer.testing import CliRunner
from retro_todo.ui.main import app

runner = CliRunner()

def test_my_command():
    result = runner.invoke(app, ["my-command", "test-arg"])
    assert result.exit_code == 0
    assert "Received: test-arg" in result.output
```

### Task 4: Style Output with Rich

```python
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()

# Styled text
console.print("[cyan]Header[/cyan] with [green]colors[/green]")

# Table
table = Table(title="My Table", border_style="cyan")
table.add_column("ID", style="magenta")
table.add_column("Name", style="green")
table.add_row("1", "Task A")
console.print(table)

# Panel
panel = Panel("Content", title="Title", border_style="yellow")
console.print(panel)
```

### Task 5: Interactive Prompt with Questionary

```python
import questionary
from retro_todo.ui.theme import retro_style

# Text input
answer = questionary.text(
    "What is your name?",
    style=retro_style
).ask()

# Select menu
choice = questionary.select(
    "Choose priority:",
    choices=["Low", "Medium", "High", "Urgent"],
    style=retro_style
).ask()

# Confirmation
confirmed = questionary.confirm(
    "Are you sure?",
    default=False,
    style=retro_style
).ask()
```

---

## Debugging Tips

### Enable Debug Logging

```python
# Add to top of file
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Inspect Database Contents

```bash
# View raw JSON
cat todo_data.json | python -m json.tool

# Or use Python REPL
uv run python
>>> from retro_todo.database.db import tasks_table
>>> tasks_table.all()
```

### Run Single Test with Print Statements

```bash
# -s flag shows print() output
uv run pytest tests/unit/test_models.py::test_title_validation -s
```

### Check Coverage for Specific Module

```bash
uv run pytest --cov=retro_todo.services.todo_service --cov-report=term-missing
```

---

## Code Style Guidelines

### Type Hints (Required)

```python
# ✅ Good - type hints on all parameters and return
def add_task(title: str, priority: Priority) -> TodoTask:
    ...

# ❌ Bad - no type hints
def add_task(title, priority):
    ...
```

### Docstrings (Required for Public APIs)

```python
# ✅ Good - clear docstring
def search_tasks(query: str) -> list[TodoTask]:
    """
    Search tasks by keyword in title or description.
    
    Args:
        query: Search term (case-insensitive)
        
    Returns:
        List of matching tasks, ordered by relevance
    """
    ...
```

### Pydantic v2 Syntax (Required)

```python
# ✅ Good - v2 syntax
@field_validator('title')
@classmethod
def title_not_empty(cls, v: str) -> str:
    ...

# ❌ Bad - v1 syntax (deprecated)
@validator('title')
def title_not_empty(cls, v: str) -> str:
    ...
```

---

## Troubleshooting

### Issue: `uv: command not found`

**Solution**: Install uv via instructions above, ensure it's in PATH

### Issue: Import errors when running tests

**Solution**: Always use `uv run pytest` (not just `pytest`)

### Issue: Database file locked

**Solution**: Close other instances of the app, or delete `todo_data.json`

### Issue: Tests fail with validation errors

**Solution**: Check Pydantic v2 syntax, ensure `@classmethod` decorator present

### Issue: Coverage below 80%

**Solution**: Add tests for uncovered lines (see `--cov-report=term-missing`)

---

## Resources

- **Constitution**: `.specify/memory/constitution.md` - Project principles
- **Specification**: `specs/001-retro-todo-app/spec.md` - Feature requirements
- **Plan**: `specs/001-retro-todo-app/plan.md` - Implementation architecture
- **Data Models**: `specs/001-retro-todo-app/data-model.md` - Pydantic schemas
- **CLI Contracts**: `specs/001-retro-todo-app/contracts/cli-commands.md` - Command specs

### External Documentation

- [uv Docs](https://github.com/astral-sh/uv)
- [Pydantic v2 Guide](https://docs.pydantic.dev/latest/)
- [Typer Tutorial](https://typer.tiangolo.com/)
- [Rich Documentation](https://rich.readthedocs.io/)
- [Textual Guide](https://textual.textualize.io/)
- [Questionary Docs](https://questionary.readthedocs.io/)
- [TinyDB Usage](https://tinydb.readthedocs.io/)

---

## Next Steps

1. **Read the Constitution**: Understand the 6 core principles
2. **Read the Specification**: Familiarize with user stories and requirements
3. **Run Tests**: Verify your environment is set up correctly
4. **Pick a Task**: Check `specs/001-retro-todo-app/tasks.md` (once created)
5. **Follow TDD**: Write test → Make it pass → Refactor

**Welcome to the team! Let's build something mind-blowing. 🎮**

---

**Developer by: maneeshanif**
