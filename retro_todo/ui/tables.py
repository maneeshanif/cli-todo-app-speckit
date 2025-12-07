"""
Rich table rendering for task display.

Provides formatted tables for task lists and statistics panels.

T033, T059, T071: GREEN phase implementation.
"""
import re
from typing import List, Dict, Any, Optional

from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.console import Group
from rich import box

from retro_todo.models.todo import TodoTask
from retro_todo.models.enums import Priority, Status
from .theme import COLORS


def format_task_table(tasks: List[TodoTask], show_all: bool = True) -> Table:
    """
    Create a Rich table displaying tasks.
    
    Args:
        tasks: List of TodoTask objects to display
        show_all: Whether to show all columns or a compact view
        
    Returns:
        Rich Table instance
    """
    table = Table(
        title="[bold cyan]📋 TASK LIST[/bold cyan]",
        box=box.DOUBLE_EDGE,
        border_style="cyan",
        header_style="bold magenta",
        row_styles=["", "dim"],
        show_lines=True,
    )
    
    # Add columns
    table.add_column("ID", justify="center", style="cyan", width=6)
    table.add_column("Title", style="white", min_width=20, max_width=40)
    table.add_column("Priority", justify="center", width=12)
    table.add_column("Status", justify="center", width=12)
    
    if show_all:
        table.add_column("Tags", style="cyan", width=20)
        table.add_column("Due Date", width=20)
    
    # Add rows
    for task in tasks:
        row = [
            str(task.id),
            _format_title(task),
            task.format_priority_badge(),
            task.format_status_badge(),
        ]
        
        if show_all:
            row.extend([
                task.format_tags_display(),
                task.format_due_date_display(),
            ])
        
        table.add_row(*row)
    
    return table


def _format_title(task: TodoTask) -> str:
    """Format task title with status styling."""
    if task.status == Status.COMPLETED:
        return f"[strike dim]{task.title}[/strike dim]"
    return task.title


def format_single_task(task: TodoTask) -> Panel:
    """
    Create a detailed view panel for a single task.
    
    Args:
        task: TodoTask to display in detail
        
    Returns:
        Rich Panel with task details
    """
    content = Text()
    
    content.append(f"ID: ", style="dim")
    content.append(f"{task.id}\n", style="cyan bold")
    
    content.append(f"Title: ", style="dim")
    content.append(f"{task.title}\n", style="white bold")
    
    if task.description:
        content.append(f"\nDescription:\n", style="dim")
        content.append(f"{task.description}\n", style="white")
    
    content.append(f"\nPriority: ", style="dim")
    content.append(f"{task.priority.icon} {task.priority.value.upper()}\n", 
                   style=task.priority.color)
    
    content.append(f"Status: ", style="dim")
    content.append(f"{task.status.icon} {task.status.value.capitalize()}\n",
                   style="green" if task.status == Status.COMPLETED else "yellow")
    
    content.append(f"\nTags: ", style="dim")
    content.append(task.format_tags_display() + "\n")
    
    content.append(f"Due Date: ", style="dim")
    content.append(task.format_due_date_display() + "\n")
    
    if task.has_recurrence():
        content.append(f"Recurrence: ", style="dim")
        content.append(task.recurrence_pattern.display_label + "\n", style="magenta")
    
    content.append(f"\nCreated: ", style="dim")
    content.append(f"{task.created_at.strftime('%Y-%m-%d %H:%M')}\n", style="dim")
    
    return Panel(
        content,
        title=f"[bold cyan]📝 Task #{task.id}[/bold cyan]",
        border_style="cyan",
        padding=(1, 2),
    )


def format_stats_panel(stats: Dict[str, Any]) -> Panel:
    """
    Create a statistics panel.
    
    Args:
        stats: Dictionary with task statistics
        
    Returns:
        Rich Panel with statistics display
    """
    content = Text()
    
    # Overview section
    content.append("📊 OVERVIEW\n", style="bold magenta")
    content.append("─" * 30 + "\n", style="dim")
    content.append(f"Total Tasks: ", style="dim")
    content.append(f"{stats.get('total', 0)}\n", style="cyan bold")
    content.append(f"Completed: ", style="dim")
    content.append(f"{stats.get('completed', 0)}\n", style="green")
    content.append(f"Pending: ", style="dim")
    content.append(f"{stats.get('pending', 0)}\n", style="yellow")
    content.append(f"Overdue: ", style="dim")
    content.append(f"{stats.get('overdue', 0)}\n", style="red")
    
    # Priority breakdown
    by_priority = stats.get('by_priority', {})
    if by_priority:
        content.append("\n📈 BY PRIORITY\n", style="bold magenta")
        content.append("─" * 30 + "\n", style="dim")
        for priority in Priority:
            count = by_priority.get(priority.value, 0)
            content.append(f"{priority.icon} {priority.value.upper()}: ", 
                          style=priority.color)
            content.append(f"{count}\n", style="white")
    
    # Tag breakdown
    by_tags = stats.get('by_tags', {})
    if by_tags:
        content.append("\n🏷️ BY TAGS\n", style="bold magenta")
        content.append("─" * 30 + "\n", style="dim")
        for tag, count in sorted(by_tags.items(), key=lambda x: -x[1])[:10]:
            content.append(f"#{tag}: ", style="cyan")
            content.append(f"{count}\n", style="white")
    
    return Panel(
        content,
        title="[bold cyan]📊 STATISTICS[/bold cyan]",
        border_style="magenta",
        padding=(1, 2),
    )


def highlight_search_term(text: str, search_term: str) -> str:
    """
    Highlight search term in text with Rich markup.
    
    Args:
        text: Original text
        search_term: Term to highlight
        
    Returns:
        Text with Rich markup for highlighting
    """
    if not search_term:
        return text
    
    # Case insensitive replacement
    pattern = re.compile(re.escape(search_term), re.IGNORECASE)
    
    def replace_match(match):
        return f"[bold yellow on black]{match.group()}[/bold yellow on black]"
    
    return pattern.sub(replace_match, text)


def format_empty_state(message: str = "No tasks found") -> Panel:
    """
    Display an empty state message.
    
    Args:
        message: Custom message to display
        
    Returns:
        Rich Panel with empty state
    """
    content = Text()
    content.append("🎮 ", style="yellow")
    content.append(message, style="dim")
    content.append(" 🎮", style="yellow")
    content.append("\n\n")
    content.append("Use ", style="dim")
    content.append("retro-todo add", style="green")
    content.append(" to create your first task!", style="dim")
    
    return Panel(
        content,
        title="[cyan]Empty[/cyan]",
        border_style="dim",
        padding=(1, 2),
    )


def format_diff(before: TodoTask, after: TodoTask) -> Panel:
    """
    Display a diff between task states.
    
    Args:
        before: Original task state
        after: Updated task state
        
    Returns:
        Rich Panel showing changes
    """
    content = Text()
    content.append("📝 CHANGES\n", style="bold magenta")
    content.append("─" * 30 + "\n", style="dim")
    
    fields = ['title', 'description', 'priority', 'status', 'tags', 'due_date']
    
    for field in fields:
        old_val = getattr(before, field)
        new_val = getattr(after, field)
        
        if old_val != new_val:
            content.append(f"{field.title()}: ", style="cyan")
            content.append(f"{old_val}", style="red strike")
            content.append(" → ", style="dim")
            content.append(f"{new_val}\n", style="green")
    
    return Panel(
        content,
        title="[bold cyan]🔄 Task Updated[/bold cyan]",
        border_style="green",
        padding=(1, 2),
    )
