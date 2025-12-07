"""
Questionary interactive prompts for Retro Todo.

Provides styled forms for task input and user interactions.

T035, T055, T057, T073, T081, T083: GREEN phase implementation.
"""
from typing import Optional, Dict, Any, List
from datetime import datetime

import questionary
from dateutil.parser import parse, ParserError

from retro_todo.models.enums import Priority, Status, RecurrencePattern
from .theme import retro_style


def add_task_prompt() -> Optional[Dict[str, Any]]:
    """
    Interactive prompt for adding a new task.
    
    Returns:
        Dictionary with task data or None if cancelled
    """
    # Get title (required)
    title = questionary.text(
        "Task title:",
        style=retro_style,
        validate=lambda x: len(x.strip()) > 0 or "Title cannot be empty"
    ).ask()
    
    if title is None:
        return None
    
    # Get priority
    priority = questionary.select(
        "Priority level:",
        choices=[
            questionary.Choice(f"{p.icon} {p.value.upper()}", value=p.value)
            for p in Priority
        ],
        style=retro_style,
        default=Priority.MEDIUM.value
    ).ask()
    
    if priority is None:
        return None
    
    # Get description (optional)
    description = questionary.text(
        "Description (optional):",
        style=retro_style,
    ).ask()
    
    if description is None:
        return None
    
    # Get tags (optional)
    tags_input = questionary.text(
        "Tags (comma-separated, optional):",
        style=retro_style,
    ).ask()
    
    if tags_input is None:
        return None
    
    tags = [t.strip() for t in tags_input.split(",") if t.strip()] if tags_input else []
    
    # Get due date (optional)
    due_date = _prompt_due_date()
    
    # Get recurrence (optional)
    recurrence = questionary.select(
        "Recurrence pattern:",
        choices=[
            questionary.Choice("None (one-time)", value=RecurrencePattern.NONE.value),
            questionary.Choice("🔁 Daily", value=RecurrencePattern.DAILY.value),
            questionary.Choice("🔁 Weekly", value=RecurrencePattern.WEEKLY.value),
            questionary.Choice("🔁 Monthly", value=RecurrencePattern.MONTHLY.value),
        ],
        style=retro_style,
        default=RecurrencePattern.NONE.value
    ).ask()
    
    if recurrence is None:
        return None
    
    return {
        "title": title.strip(),
        "description": description.strip() if description else None,
        "priority": Priority(priority),
        "tags": tags,
        "due_date": due_date,
        "recurrence_pattern": RecurrencePattern(recurrence),
    }


def _prompt_due_date() -> Optional[datetime]:
    """Prompt for due date with natural language support."""
    date_input = questionary.text(
        "Due date (e.g., 'tomorrow', 'next Friday', '2025-12-25', or leave empty):",
        style=retro_style,
    ).ask()
    
    if not date_input or not date_input.strip():
        return None
    
    try:
        # Try to parse natural language date
        parsed = parse(date_input, fuzzy=True)
        # Confirm the parsed date
        confirm = questionary.confirm(
            f"Due date: {parsed.strftime('%Y-%m-%d %H:%M')}. Is this correct?",
            style=retro_style,
            default=True
        ).ask()
        
        if confirm:
            return parsed
        else:
            # Ask for explicit format
            explicit = questionary.text(
                "Enter date (YYYY-MM-DD HH:MM):",
                style=retro_style,
            ).ask()
            if explicit:
                return datetime.fromisoformat(explicit)
    except (ParserError, ValueError):
        # Ask for explicit format on parse failure
        from rich.console import Console
        Console().print("[yellow]⚠️ Could not parse date[/yellow]")
        explicit = questionary.text(
            "Enter date (YYYY-MM-DD):",
            style=retro_style,
        ).ask()
        if explicit:
            try:
                return datetime.fromisoformat(explicit)
            except ValueError:
                return None
    
    return None


def update_task_prompt(current_task) -> Optional[Dict[str, Any]]:
    """
    Interactive prompt for updating a task.
    
    Args:
        current_task: Current TodoTask to update
        
    Returns:
        Dictionary with updated fields or None if cancelled
    """
    # Ask which fields to update
    fields = questionary.checkbox(
        "Select fields to update:",
        choices=[
            questionary.Choice("Title", value="title"),
            questionary.Choice("Description", value="description"),
            questionary.Choice("Priority", value="priority"),
            questionary.Choice("Tags", value="tags"),
            questionary.Choice("Due Date", value="due_date"),
            questionary.Choice("Recurrence", value="recurrence_pattern"),
        ],
        style=retro_style,
    ).ask()
    
    if not fields:
        return None
    
    updates = {}
    
    if "title" in fields:
        title = questionary.text(
            "New title:",
            default=current_task.title,
            style=retro_style,
        ).ask()
        if title is None:
            return None
        updates["title"] = title.strip()
    
    if "description" in fields:
        desc = questionary.text(
            "New description:",
            default=current_task.description or "",
            style=retro_style,
        ).ask()
        if desc is None:
            return None
        updates["description"] = desc.strip() if desc else None
    
    if "priority" in fields:
        priority = questionary.select(
            "New priority:",
            choices=[f"{p.icon} {p.value.upper()}" for p in Priority],
            style=retro_style,
        ).ask()
        if priority is None:
            return None
        # Extract priority value from selection
        priority_value = priority.split()[-1].lower()
        updates["priority"] = Priority(priority_value)
    
    if "tags" in fields:
        current_tags = ", ".join(current_task.tags) if current_task.tags else ""
        tags_input = questionary.text(
            "New tags (comma-separated):",
            default=current_tags,
            style=retro_style,
        ).ask()
        if tags_input is None:
            return None
        updates["tags"] = [t.strip() for t in tags_input.split(",") if t.strip()]
    
    if "due_date" in fields:
        updates["due_date"] = _prompt_due_date()
    
    if "recurrence_pattern" in fields:
        recurrence = questionary.select(
            "New recurrence:",
            choices=[
                questionary.Choice("None", value=RecurrencePattern.NONE.value),
                questionary.Choice("Daily", value=RecurrencePattern.DAILY.value),
                questionary.Choice("Weekly", value=RecurrencePattern.WEEKLY.value),
                questionary.Choice("Monthly", value=RecurrencePattern.MONTHLY.value),
            ],
            style=retro_style,
        ).ask()
        if recurrence is None:
            return None
        updates["recurrence_pattern"] = RecurrencePattern(recurrence)
    
    return updates


def filter_prompt() -> Dict[str, Any]:
    """
    Interactive prompt for filtering tasks.
    
    Returns:
        Dictionary with filter criteria
    """
    filters = {}
    
    # Priority filter
    priorities = questionary.checkbox(
        "Filter by priority (select multiple or none for all):",
        choices=[f"{p.icon} {p.value.upper()}" for p in Priority],
        style=retro_style,
    ).ask()
    
    if priorities:
        filters["priorities"] = [
            Priority(p.split()[-1].lower()) for p in priorities
        ]
    
    # Status filter
    status = questionary.select(
        "Filter by status:",
        choices=[
            questionary.Choice("All", value=None),
            questionary.Choice("⏳ Pending", value=Status.PENDING),
            questionary.Choice("✅ Completed", value=Status.COMPLETED),
        ],
        style=retro_style,
    ).ask()
    
    if status:
        filters["status"] = status
    
    # Tag filter
    tags_input = questionary.text(
        "Filter by tags (comma-separated, leave empty for all):",
        style=retro_style,
    ).ask()
    
    if tags_input and tags_input.strip():
        filters["tags"] = [t.strip().lower() for t in tags_input.split(",") if t.strip()]
    
    return filters


def confirm_delete(task_title: str) -> bool:
    """
    Confirm task deletion.
    
    Args:
        task_title: Title of task to delete
        
    Returns:
        True if user confirms deletion
    """
    return questionary.confirm(
        f"Are you sure you want to delete '{task_title}'?",
        style=retro_style,
        default=False
    ).ask() or False


def select_task_prompt(tasks: List, action: str = "select") -> Optional[int]:
    """
    Prompt user to select a task from list.
    
    Args:
        tasks: List of TodoTask objects
        action: Action being performed (for message)
        
    Returns:
        Selected task ID or None
    """
    if not tasks:
        return None
    
    choices = [
        questionary.Choice(
            f"[{t.id}] {t.priority.icon} {t.title}",
            value=t.id
        )
        for t in tasks
    ]
    
    return questionary.select(
        f"Select task to {action}:",
        choices=choices,
        style=retro_style,
    ).ask()


def search_prompt() -> Optional[str]:
    """
    Prompt for search term.
    
    Returns:
        Search query or None
    """
    return questionary.text(
        "Search tasks:",
        style=retro_style,
    ).ask()
