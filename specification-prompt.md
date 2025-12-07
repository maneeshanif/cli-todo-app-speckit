# Specification Prompt for Retro Todo CLI

> **Usage:** Copy the content below and run `/sp.specify` in Claude Code to create feature specifications.

---

## Input for `/sp.specify`

```text
Build a mind-blowing Retro Terminal Todo Manager - a multi-page TUI application with cyberpunk aesthetics that manages tasks with full CRUD, search, filter, sort, recurring tasks, and reminders.

## Feature: Complete Retro Todo Application (Phase I)

### User Personas
- **Developer**: Wants a fast, keyboard-driven todo app with visual appeal
- **Terminal Enthusiast**: Loves retro aesthetics and ASCII art
- **Power User**: Needs advanced features like recurring tasks and filters

### Core Features (10 Total)

#### 🟩 Basic Level (Points: 40)
1. **Add Task** (8 pts)
   - Title (required), description (optional)
   - Priority: Low, Medium, High, Urgent (with colors)
   - Tags: comma-separated custom tags
   - Due date with natural language parsing ("tomorrow", "next week")
   - Rich panel confirmation with task preview

2. **Delete Task** (8 pts)
   - Questionary confirmation prompt
   - Show task details before deletion
   - Success animation with Rich

3. **Update Task** (8 pts)
   - Select task from Rich table
   - Questionary form for field updates
   - Show before/after diff

4. **View Task List** (8 pts)
   - Rich table with colored priority columns
   - Status icons: ⏳ pending, ✅ complete, ⚠️ overdue
   - Sortable columns
   - Progress bar showing completion %

5. **Mark Complete** (8 pts)
   - Toggle completion with animation
   - Strike-through for completed tasks
   - Completion celebration effect

#### 🟦 Intermediate Level (Points: 30)
6. **Priorities & Tags** (10 pts)
   - Priority colors: 🔴 Urgent, 🟠 High, 🟡 Medium, 🟢 Low
   - Tag filtering with autocomplete
   - Tag statistics panel

7. **Search & Filter** (10 pts)
   - Fuzzy search by title/description
   - Filter by: priority, status, tags, date range
   - Combined filters with AND/OR logic
   - Highlighted search results

8. **Sort Tasks** (10 pts)
   - Sort by: priority, due date, created date, title
   - Ascending/descending toggle
   - Persist sort preference

#### 🟥 Advanced Level (Points: 30)
9. **Recurring Tasks** (15 pts)
   - Patterns: daily, weekly, monthly, custom
   - Auto-generate next occurrence on completion
   - Recurrence indicator in list view

10. **Due Dates & Reminders** (15 pts)
    - Due date with time support
    - Overdue highlighting
    - "Due today" and "Due this week" quick filters
    - Countdown display for urgent tasks

### UI/UX Requirements

#### Splash Screen (MUST HAVE)
```
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║   ████████╗ ██████╗ ██████╗  ██████╗                        ║
║   ╚══██╔══╝██╔═══██╗██╔══██╗██╔═══██╗                       ║
║      ██║   ██║   ██║██║  ██║██║   ██║                       ║
║      ██║   ╚██████╔╝██████╔╝╚██████╔╝                       ║
║      ╚═╝    ╚═════╝ ╚═════╝  ╚═════╝                        ║
║                                                              ║
║            🎮 RETRO TERMINAL TASK MANAGER 🎮                ║
║                     Version 1.0.0                            ║
║                                                              ║
║              ═══════════════════════════                     ║
║                Developer by: maneeshanif                     ║
║              ═══════════════════════════                     ║
║                                                              ║
║     [Press ENTER to continue or Q to quit]                   ║
╚══════════════════════════════════════════════════════════════╝
```

#### Color Theme (Cyberpunk Retro)
- Primary: Cyan (#00FFFF) - Headers, borders
- Secondary: Magenta (#FF00FF) - Highlights, selections
- Success: Bright Green (#00FF00) - Completed tasks
- Warning: Yellow (#FFFF00) - Due soon
- Error: Red (#FF0000) - Overdue, errors
- Background accents: Dark blue (#000033)

#### Navigation
- Typer commands: `todo add`, `todo list`, `todo delete`, etc.
- Arrow keys for selection in Textual TUI
- Vim-style shortcuts (j/k for up/down)
- ESC to go back, Q to quit

### Data Model

```python
class Priority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"

class Status(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"

class RecurrencePattern(str, Enum):
    NONE = "none"
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"

class TodoTask(BaseModel):
    id: int
    title: str
    description: str = ""
    priority: Priority = Priority.MEDIUM
    status: Status = Status.PENDING
    tags: list[str] = []
    due_date: datetime | None = None
    recurrence: RecurrencePattern = RecurrencePattern.NONE
    created_at: datetime
    updated_at: datetime
    completed_at: datetime | None = None
```

### Technical Stack

| Library | Usage |
|---------|-------|
| typer[all] | CLI commands with `--help` |
| rich | Tables, panels, progress bars, syntax highlighting |
| textual | Multi-page TUI application |
| pydantic | TodoTask model with validation |
| tinydb | JSON storage with CachingMiddleware |
| questionary | Interactive prompts with styling |
| pyfiglet | ASCII art splash screen |
| python-dateutil | Natural language date parsing |

### Acceptance Criteria

- [ ] All 10 features implemented and working
- [ ] Splash screen displays on startup with developer credit
- [ ] Rich tables show all task fields with colors
- [ ] Questionary prompts for all user input
- [ ] TinyDB persists data between sessions
- [ ] Keyboard navigation works throughout
- [ ] Retro color theme consistently applied
- [ ] Tests cover >80% of code
- [ ] No pip usage - uv only
```

---

## Expected Output

After running `/sp.specify` with the above input, the agent will:

1. Generate a branch name (e.g., `1-retro-todo-app`)
2. Create `specs/1-retro-todo-app/spec.md` with full requirements
3. Set up the feature directory structure

---

## Quick Copy Version

For fast use, copy just this:

```
Retro Terminal Todo Manager - 10 features: Add/Delete/Update/View/Complete tasks, Priorities & Tags, Search & Filter, Sort, Recurring Tasks, Due Dates & Reminders. Stack: typer, rich, textual, pydantic, tinydb, questionary, pyfiglet. Must show "Developer by: maneeshanif" splash screen. Cyberpunk color theme (cyan, magenta, green). Phase I hackathon project due Dec 7, 2025.
```
