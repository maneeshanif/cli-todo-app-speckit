# 🎮 RETRO TODO

<div align="center">

```
    ____  ________________  ____     __________  ____  ____  
   / __ \/ ____/_  __/ __ \/ __ \   /_  __/ __ \/ __ \/ __ \ 
  / /_/ / __/   / / / /_/ / / / /    / / / / / / / / / / / / 
 / _, _/ /___  / / / _, _/ /_/ /    / / / /_/ / /_/ / /_/ /  
/_/ |_/_____/ /_/ /_/ |_|\____/    /_/  \____/_____/\____/   
```

**A mind-blowing retro terminal todo manager with cyberpunk aesthetics** 🕹️

[![Python 3.12+](https://img.shields.io/badge/python-3.12+-cyan.svg?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-magenta.svg?style=for-the-badge)](LICENSE)
[![Tests](https://img.shields.io/badge/tests-176%20passed-green.svg?style=for-the-badge)](tests/)
[![Coverage](https://img.shields.io/badge/coverage-76%25-yellow.svg?style=for-the-badge)](tests/)

</div>

---

## ✨ Features

🎨 **Cyberpunk Aesthetics** - Stunning retro terminal UI with neon colors and ASCII art

📝 **Full Task Management** - Create, read, update, delete tasks with ease

🏷️ **Tags & Priorities** - Organize tasks with custom tags and priority levels (🟢 Low, 🟡 Medium, 🟠 High, 🔴 Urgent)

🔍 **Smart Search** - Find tasks instantly with powerful search

📊 **Statistics Dashboard** - Track your productivity with beautiful stats

🎉 **Celebrations** - Get rewarded with animations when completing tasks

⚡ **Lightning Fast** - Built with TinyDB for blazing fast local storage

🎮 **Interactive Menu** - Single app experience - start once, do everything!

---

## 🚀 Quick Start

### Prerequisites

- Python 3.12 or higher
- [uv](https://github.com/astral-sh/uv) package manager (recommended)

### Installation

```bash
# Clone the repository
git clone https://github.com/maneeshanif/cli-todo-app-speckit.git
cd cli-todo-app-speckit

# Install dependencies with uv
uv sync

# Install the package
uv pip install -e .
```

### 🎮 Run the App

```bash
uv run todo
```

**That's it!** The app launches and you're in control. Navigate with arrow keys and Enter.

---

## 📖 Usage Guide

### Starting the App

```bash
uv run todo
```

You'll see the epic splash screen followed by the main menu:

```
? What would you like to do? (Use ↑↓ arrows, Enter to select)
❯ 📋  View All Tasks
  ➕  Add New Task
  ✅  Complete a Task
  ✏️   Edit a Task
  🗑️   Delete a Task
  🔍  Search Tasks
  📊  View Statistics
  ─────────────────
  🚪  Exit
```

### Navigation

| Key | Action |
|-----|--------|
| ↑ / ↓ | Move through menu/list |
| Enter | Select option |
| Ctrl+C | Force quit |

---

### ➕ Adding Tasks

Select "Add New Task" and fill in the details:

```
? Task title: Buy groceries
? Description (optional): Milk, eggs, bread
? Priority:
  🟢 Low
❯ 🟡 Medium
  🟠 High
  🔴 Urgent
? Tags (comma-separated): shopping, food
```

#### Priority Levels

| Priority | Icon | When to use |
|----------|------|-------------|
| Low | 🟢 | Someday/maybe tasks |
| Medium | 🟡 | Normal tasks (default) |
| High | 🟠 | Important tasks |
| Urgent | 🔴 | Do immediately! |

---

### 📋 Viewing Tasks

Beautiful tables with all your tasks:

```
┏━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━━━┓
┃  ID  ┃ Title                ┃ Priority ┃  Status  ┃    Tags    ┃
┡━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━━━┩
│  #1  │ Buy groceries        │ 🟡 Med   │ ⏳ Pend  │ shopping   │
│  #2  │ Complete project     │ 🔴 Urg   │ ⏳ Pend  │ work       │
│  #3  │ Call mom             │ 🟢 Low   │ ✅ Done  │ family     │
└──────┴──────────────────────┴──────────┴──────────┴────────────┘
```

#### Filter Options

| Filter | Shows |
|--------|-------|
| 📋 All Tasks | Everything |
| ⏳ Pending Only | Incomplete tasks |
| ✅ Completed Only | Finished tasks |
| 🔴 Urgent Priority | Urgent tasks only |
| 🟠 High Priority | High priority only |
| 🟡 Medium Priority | Medium priority only |
| 🟢 Low Priority | Low priority only |

---

### ✅ Completing Tasks

Select a task to mark as complete and get a celebration!

```
╭────────────────────────────────────────────────────────────────────╮
│    🎉 TASK COMPLETED! 🎉                                           │
│    ✅ Buy groceries                                                │
│    🌟 Great job! 🌟                                                │
╰────────────────────────────────────────────────────────────────────╯
```

---

### ✏️ Editing Tasks

Update any aspect of your tasks:

```
? What would you like to edit?
❯ 📝 Title
  📄 Description
  🎯 Priority
  🏷️  Tags
  ← Back to menu
```

---

### 🗑️ Deleting Tasks

You'll be asked to confirm before deletion:

```
? Are you sure you want to delete "Buy groceries"? (y/N)
```

⚠️ Deleted tasks **cannot be recovered**

---

### 🔍 Searching Tasks

Find tasks by keywords in title, description, or tags:

```
? Enter search term: shopping
```

---

### 📊 Statistics

Track your productivity:

```
╭──────────────────── 📊 STATISTICS ────────────────────╮
│                                                       │
│   Total Tasks:     10                                 │
│   Completed:       6  (60%)                           │
│   Pending:         4  (40%)                           │
│                                                       │
│   ████████████░░░░░░░░  60%                          │
│                                                       │
│   Priority Breakdown:                                 │
│   🔴 Urgent:  2                                       │
│   🟠 High:    3                                       │
│   🟡 Medium:  3                                       │
│   🟢 Low:     2                                       │
│                                                       │
╰───────────────────────────────────────────────────────╯
```

---

### 🚪 Exiting

Select "Exit" to leave with a friendly goodbye:

```
╭────────────────────────────────────────────────────────╮
│   👋 Thanks for using RETRO TODO!                      │
│   🎮 Keep crushing those tasks! 🎮                     │
╰────────────────────────────────────────────────────────╯
```

---

## 💾 Data Storage

Tasks are saved locally in:
```
~/.retro-todo/tasks.db
```

All changes save automatically - no manual save required!

---

## 🛠️ Alternative Installation (pip)

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the app
python -m retro_todo.app
```

---

## 🧪 Development

### Run Tests

```bash
uv run pytest
```

### Test Coverage

```bash
uv run pytest --cov=retro_todo --cov-report=html
```

### Project Structure

```
retro-todo/
├── retro_todo/
│   ├── __init__.py          # Package info
│   ├── app.py               # 🎮 Interactive app
│   ├── models/              # Pydantic models
│   ├── database/            # TinyDB operations
│   ├── services/            # Business logic
│   └── ui/                  # Rich UI components
├── tests/                   # 176 passing tests
├── pyproject.toml
├── README.md
└── LICENSE
```

---

## 🎨 Tech Stack

| Technology | Purpose |
|------------|---------|
| **Python 3.12** | Core language |
| **Pydantic** | Data validation |
| **TinyDB** | Local JSON database |
| **Rich** | Terminal UI |
| **Questionary** | Interactive prompts |

---

## 📝 License

MIT License - see [LICENSE](LICENSE)

---

## 👨‍💻 Author

**maneeshanif**

---

<div align="center">

```
╔══════════════════════════════════════════════════════════════╗
║   🎮  START CRUSHING YOUR TASKS TODAY!  🎮                   ║
║                                                              ║
║   uv run todo                                                ║
╚══════════════════════════════════════════════════════════════╝
```

**Made with 💜 and lots of ☕**

</div>
