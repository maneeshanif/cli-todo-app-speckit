# CLI Command Contracts: Retro Terminal Todo Manager

**Feature**: 001-retro-todo-app  
**Date**: 2025-12-07  
**Phase**: 1 (Design)

## Overview

This document specifies all CLI commands, their parameters, outputs, and error behaviors. All commands follow Typer framework conventions with Rich markup support.

---

## Command Tree

```
retro-todo (entry point)
├── splash            # Show splash screen (default if no command)
├── add               # Create new task
├── list              # Display tasks
├── view <id>         # Show task details
├── update <id>       # Modify existing task
├── complete <id>     # Mark task as done
├── delete <id>       # Remove task
├── search <query>    # Find tasks by keyword
├── filter            # Apply filters (interactive)
├── sort <key>        # Sort task list
└── stats             # Show statistics dashboard
```

---

## Command Specifications

### `retro-todo` (Default)

**Purpose**: Show splash screen and main menu.

**Signature**:
```python
@app.command()
def splash():
    """[cyan]Display retro splash screen[/cyan] and main menu."""
```

**Inputs**: None

**Output**:
```
┌─────────────────────────────────────────────┐
│                                             │
│    ______  ____  ____  ____                │
│   /_  __/ / __ \/ __ \/ __ \               │
│    / /   / / / / / / / / / /               │
│   / /   / /_/ / /_/ / /_/ /                │
│  /_/    \____/_____/\____/                 │
│                                             │
│  🎮 RETRO TASK MANAGER                     │
│  Developer by: maneeshanif                 │
│                                             │
└─────────────────────────────────────────────┘

[cyan]Available Commands:[/cyan]
  add      - Create new task
  list     - Display all tasks
  search   - Find tasks
  stats    - View statistics

Press [magenta]Enter[/magenta] to continue or [yellow]Q[/yellow] to quit
```

**Exit Codes**:
- 0: Success

---

### `retro-todo add`

**Purpose**: Create a new task with interactive prompts.

**Signature**:
```python
@app.command()
def add(
    title: Optional[str] = typer.Option(None, "--title", "-t", help="Task title"),
    quick: bool = typer.Option(False, "--quick", "-q", help="Skip optional fields")
):
    """[cyan]Add a new task[/cyan] with full details."""
```

**Interactive Prompts** (if not provided via options):
1. Title (required) - text input
2. Description (optional) - text input
3. Priority (optional, default: Medium) - select menu
4. Tags (optional) - text input (comma-separated)
5. Due date (optional) - text input (natural language)
6. Recurrence (optional, default: None) - select menu

**Output (Success)**:
```
[green]✓[/green] Task created successfully

┌─────────────────────────────────────────────┐
│ Task #42                                    │
├─────────────────────────────────────────────┤
│ Title:       Fix login bug                  │
│ Priority:    🔴 URGENT                      │
│ Status:      ⏳ Pending                     │
│ Tags:        #backend #security             │
│ Due Date:    📅 2025-12-08 14:00           │
│ Recurrence:  None                           │
│ Created:     2025-12-07 10:30              │
└─────────────────────────────────────────────┘
```

**Validation Errors**:
- Title empty: `[red]✗[/red] Title cannot be empty`
- Due date in past: `[red]✗[/red] Due date cannot be in the past`
- Invalid recurrence: `[red]✗[/red] Invalid recurrence pattern`

**Exit Codes**:
- 0: Success
- 1: Validation error

---

### `retro-todo list`

**Purpose**: Display all tasks in formatted table.

**Signature**:
```python
@app.command()
def list(
    status: Optional[str] = typer.Option(None, "--status", "-s", help="Filter by status (pending/completed)"),
    priority: Optional[str] = typer.Option(None, "--priority", "-p", help="Filter by priority"),
    limit: int = typer.Option(50, "--limit", "-n", help="Maximum tasks to display")
):
    """[cyan]List all tasks[/cyan] in a beautiful table."""
```

**Output (With Tasks)**:
```
┌──────────────────────────────────────────────────────────────────────────────┐
│                          📋 Task List (25 tasks)                             │
├────┬────────────────────┬──────────┬─────────┬────────────┬──────────────────┤
│ ID │ Title              │ Priority │ Status  │ Tags       │ Due Date         │
├────┼────────────────────┼──────────┼─────────┼────────────┼──────────────────┤
│ 42 │ Fix login bug      │ 🔴 URGENT│ ⏳ Pending│#backend   │ 📅 2025-12-08   │
│ 41 │ Write docs         │ 🟡 MEDIUM│ ⏳ Pending│#docs      │ 📅 2025-12-10   │
│ 40 │ Refactor auth      │ 🟠 HIGH  │ ✅ Done │#backend   │ -               │
└────┴────────────────────┴──────────┴─────────┴────────────┴──────────────────┘

[dim]Showing 25 of 42 tasks. Use --limit to show more.[/dim]
```

**Output (Empty State)**:
```
┌─────────────────────────────────────────────┐
│          No tasks found                     │
│                                             │
│  Get started by adding your first task:    │
│  [cyan]retro-todo add[/cyan]               │
└─────────────────────────────────────────────┘
```

**Exit Codes**:
- 0: Success

---

### `retro-todo view <id>`

**Purpose**: Show detailed view of a single task.

**Signature**:
```python
@app.command()
def view(id: int = typer.Argument(..., help="Task ID to view")):
    """[cyan]View task details[/cyan] with full information."""
```

**Output (Success)**:
```
╔═════════════════════════════════════════════╗
║              Task #42 Details               ║
╠═════════════════════════════════════════════╣
║                                             ║
║ Title:        Fix login bug                 ║
║ Description:  Users cannot login with       ║
║               Google OAuth provider         ║
║                                             ║
║ Priority:     🔴 URGENT                     ║
║ Status:       ⏳ Pending                    ║
║ Tags:         #backend #security #bug      ║
║                                             ║
║ Due Date:     📅 2025-12-08 14:00          ║
║               [yellow]⏰ 3h remaining[/yellow]         ║
║ Recurrence:   None                          ║
║                                             ║
║ Created:      2025-12-07 10:30             ║
║ Updated:      2025-12-07 10:30             ║
║ Completed:    -                             ║
║                                             ║
╚═════════════════════════════════════════════╝
```

**Error (Not Found)**:
```
[red]✗[/red] Task #999 not found
```

**Exit Codes**:
- 0: Success
- 1: Task not found

---

### `retro-todo update <id>`

**Purpose**: Modify existing task fields.

**Signature**:
```python
@app.command()
def update(
    id: int = typer.Argument(..., help="Task ID to update"),
    title: Optional[str] = typer.Option(None, "--title", "-t"),
    priority: Optional[str] = typer.Option(None, "--priority", "-p"),
    # ... other fields
):
    """[cyan]Update task fields[/cyan] with interactive prompts."""
```

**Interactive Menu** (if no options provided):
```
[magenta]What would you like to update?[/magenta]
  ❯ Title
    Description
    Priority
    Tags
    Due Date
    Recurrence
    [Done - Save Changes]
```

**Output (Success with Diff)**:
```
[green]✓[/green] Task #42 updated

[yellow]Changes:[/yellow]
  Priority:  🟡 MEDIUM  →  🔴 URGENT
  Tags:      #backend  →  #backend #security
  Due Date:  -  →  📅 2025-12-08 14:00
```

**Exit Codes**:
- 0: Success
- 1: Task not found
- 2: Validation error

---

### `retro-todo complete <id>`

**Purpose**: Mark task as completed.

**Signature**:
```python
@app.command()
def complete(id: int = typer.Argument(..., help="Task ID to complete")):
    """[cyan]Mark task as completed[/cyan] with celebration."""
```

**Output (Non-Recurring Task)**:
```
[green]✨ Task #42 completed! ✨[/green]

[dim]Title:[/dim] Fix login bug
[dim]Completed at:[/dim] 2025-12-07 15:30
```

**Output (Recurring Task)**:
```
[green]✨ Task #42 completed! ✨[/green]

[dim]Title:[/dim] Daily standup
[dim]Completed at:[/dim] 2025-12-07 09:00

[cyan]🔁 Next occurrence created:[/cyan]
[green]✓[/green] Task #43 - Daily standup
[dim]Due:[/dim] 📅 2025-12-08 09:00
```

**Animation**: Rich spinner + progress bar + confetti effect

**Exit Codes**:
- 0: Success
- 1: Task not found
- 2: Task already completed

---

### `retro-todo delete <id>`

**Purpose**: Remove task permanently.

**Signature**:
```python
@app.command()
def delete(
    id: int = typer.Argument(..., help="Task ID to delete"),
    force: bool = typer.Option(False, "--force", "-f", help="Skip confirmation")
):
    """[cyan]Delete a task[/cyan] with confirmation."""
```

**Confirmation Prompt** (unless --force):
```
[yellow]⚠️  Are you sure you want to delete this task?[/yellow]

Task #42: Fix login bug
Priority: 🔴 URGENT
Status: ⏳ Pending

[red]This action cannot be undone![/red]

  ❯ No, cancel
    Yes, delete
```

**Output (Success)**:
```
[green]✓[/green] Task #42 deleted successfully
```

**Exit Codes**:
- 0: Success
- 1: Task not found
- 2: User cancelled

---

### `retro-todo search <query>`

**Purpose**: Find tasks by keyword in title/description.

**Signature**:
```python
@app.command()
def search(
    query: str = typer.Argument(..., help="Search query"),
    case_sensitive: bool = typer.Option(False, "--case", "-c", help="Case-sensitive search")
):
    """[cyan]Search tasks[/cyan] by title or description."""
```

**Output (With Results)**:
```
[cyan]Search results for:[/cyan] "login"

┌────┬────────────────────────────────────┬──────────┬─────────┐
│ ID │ Title                              │ Priority │ Status  │
├────┼────────────────────────────────────┼──────────┼─────────┤
│ 42 │ Fix [yellow]login[/yellow] bug     │ 🔴 URGENT│ ⏳ Pend.│
│ 38 │ Update [yellow]login[/yellow] page │ 🟡 MEDIUM│ ✅ Done │
└────┴────────────────────────────────────┴──────────┴─────────┘

[dim]2 tasks found[/dim]
```

**Output (No Results)**:
```
[yellow]No tasks found matching:[/yellow] "xyz"

[dim]Try different keywords or check spelling.[/dim]
```

**Exit Codes**:
- 0: Success (even if no results)

---

### `retro-todo filter`

**Purpose**: Apply multi-criteria filters interactively.

**Signature**:
```python
@app.command()
def filter():
    """[cyan]Filter tasks[/cyan] by multiple criteria."""
```

**Interactive Menu**:
```
[magenta]Select filters to apply:[/magenta]
  ❯ ☐ Priority: Urgent
    ☐ Priority: High
    ☐ Status: Pending
    ☐ Status: Completed
    ☐ Tags: #backend
    ☐ Due Today
    ☐ Due This Week
    ☐ Overdue
    [Apply Filters]
```

**Output**: Same table format as `list` command with applied filters shown

**Exit Codes**:
- 0: Success

---

### `retro-todo sort <key>`

**Purpose**: Sort task list by specified field.

**Signature**:
```python
@app.command()
def sort(
    key: str = typer.Argument(..., help="Sort key (priority/date/title/created)"),
    reverse: bool = typer.Option(False, "--reverse", "-r", help="Descending order")
):
    """[cyan]Sort tasks[/cyan] by priority, date, or title."""
```

**Valid Keys**:
- `priority`: Sort by urgency (Urgent → High → Medium → Low)
- `date`: Sort by due date
- `title`: Alphabetical sort
- `created`: Sort by creation timestamp

**Output**: Same table format as `list` command with sort indicator in header

**Exit Codes**:
- 0: Success
- 1: Invalid sort key

---

### `retro-todo stats`

**Purpose**: Display statistics dashboard.

**Signature**:
```python
@app.command()
def stats():
    """[cyan]View statistics[/cyan] and progress dashboard."""
```

**Output**:
```
╔═══════════════════════════════════════════════╗
║           📊 Task Statistics                  ║
╠═══════════════════════════════════════════════╣
║                                               ║
║ Total Tasks:      42                          ║
║ Completed:        25 (59.5%)                  ║
║ Pending:          17 (40.5%)                  ║
║                                               ║
║ [green]██████████████████████[/green]           59.5%  ║
║                                               ║
║ By Priority:                                  ║
║   🔴 Urgent:      5                           ║
║   🟠 High:        8                           ║
║   🟡 Medium:      12                          ║
║   🟢 Low:         17                          ║
║                                               ║
║ By Tags:                                      ║
║   #backend        15                          ║
║   #frontend       10                          ║
║   #bug            7                           ║
║                                               ║
║ Overdue:          3 ⚠️                        ║
║ Due Today:        2 ⏰                        ║
║ Due This Week:    8 📅                        ║
║                                               ║
╚═══════════════════════════════════════════════╝
```

**Exit Codes**:
- 0: Success

---

## Global Options

All commands support:
- `--help, -h`: Show command help
- `--version, -v`: Show application version
- `--no-color`: Disable ANSI colors (accessibility)
- `--json`: Output in JSON format (for scripting)

---

## Error Handling

### Standard Error Format
```
[red]✗[/red] Error: <message>

[dim]Suggestion: <helpful hint>[/dim]

Use --help for more information.
```

### Common Error Codes
- 0: Success
- 1: Generic error (not found, invalid input)
- 2: Validation error
- 3: Database error (file corrupted, permission denied)
- 4: User cancelled operation

---

## Testing Considerations

Each command requires:
1. **Happy path test**: Valid inputs → expected output
2. **Edge case tests**: Empty inputs, boundary values
3. **Error tests**: Invalid IDs, malformed dates, etc.
4. **Interactive tests**: Mocked questionary responses

Example test structure:
```python
def test_add_task_with_title_option(cli_runner):
    result = cli_runner.invoke(app, ["add", "--title", "Test task"])
    assert result.exit_code == 0
    assert "Task created successfully" in result.output
```

---

## Conclusion

All 10+ commands specified with complete input/output contracts. Ready for implementation in Phase 3 by @ui-agent.

**Next**: Generate `quickstart.md` for developer onboarding.
