"""
Retro Todo CLI - Main Application Entry Point

Mind-blowing retro terminal todo manager with cyberpunk aesthetics.

T043, T044, T046, T048, T050, T063, T075, T077, T091, T093: GREEN phase implementation.

Developer by: maneeshanif
"""
import typer
from typing import Optional, List
from rich.console import Console
from datetime import datetime

from retro_todo import __version__
from retro_todo.database.db import init_database, close_database
from retro_todo.services.todo_service import TodoService
from retro_todo.models.enums import Priority, Status, RecurrencePattern
from retro_todo.ui.splash import show_splash, show_welcome_message
from retro_todo.ui.tables import (
    format_task_table, 
    format_stats_panel, 
    format_empty_state,
    format_single_task,
    highlight_search_term
)
from retro_todo.ui.prompts import (
    add_task_prompt,
    update_task_prompt,
    filter_prompt,
    confirm_delete,
    select_task_prompt,
    search_prompt
)
from retro_todo.ui.animations import (
    show_completion_celebration,
    show_success_message,
    show_error_message,
    show_warning_message,
    show_info_message
)

# Initialize Rich console
console = Console()

# Create Typer app with Rich markup support
app = typer.Typer(
    name="retro-todo",
    help="🎮 Retro Terminal Todo Manager - A mind-blowing cyberpunk task manager",
    rich_markup_mode="rich",
    add_completion=False,
)


def get_service() -> TodoService:
    """Get or initialize todo service."""
    init_database()
    return TodoService()


@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    version: bool = typer.Option(
        False, "--version", "-v", help="Show version and exit"
    ),
):
    """
    🎮 [cyan]RETRO TODO[/cyan] - Terminal Task Manager
    
    A mind-blowing retro game-style CLI todo application.
    
    [green]Developer by: maneeshanif[/green]
    """
    if version:
        console.print(f"[cyan]Retro Todo[/cyan] version [green]{__version__}[/green]")
        raise typer.Exit()
    
    if ctx.invoked_subcommand is None:
        show_splash()
        show_welcome_message()


@app.command()
def splash():
    """
    🕹️ Display the [cyan]retro splash screen[/cyan].
    """
    show_splash()


@app.command()
def add(
    title: Optional[str] = typer.Option(
        None, "--title", "-t", help="Task title"
    ),
    description: Optional[str] = typer.Option(
        None, "--description", "-d", help="Task description"
    ),
    priority: Optional[str] = typer.Option(
        None, "--priority", "-p", help="Priority: low, medium, high, urgent"
    ),
    tags: Optional[str] = typer.Option(
        None, "--tags", help="Comma-separated tags"
    ),
    interactive: bool = typer.Option(
        True, "--interactive/--no-interactive", "-i", help="Use interactive prompts"
    ),
):
    """
    ➕ [green]Add[/green] a new task.
    
    Use --no-interactive with --title for scripting.
    """
    service = get_service()
    
    if interactive and not title:
        # Interactive mode
        task_data = add_task_prompt()
        if task_data is None:
            show_warning_message("Task creation cancelled")
            raise typer.Exit()
        
        task = service.create(**task_data)
    else:
        # Non-interactive mode
        if not title:
            show_error_message("Title is required. Use --title or interactive mode.")
            raise typer.Exit(1)
        
        task_priority = Priority(priority) if priority else Priority.MEDIUM
        task_tags = [t.strip() for t in tags.split(",")] if tags else []
        
        task = service.create(
            title=title,
            description=description,
            priority=task_priority,
            tags=task_tags,
        )
    
    show_success_message(f"Task #{task.id} created: {task.title}")
    console.print(format_single_task(task))


@app.command("list")
def list_tasks(
    all_tasks: bool = typer.Option(
        False, "--all", "-a", help="Show all tasks including completed"
    ),
    pending: bool = typer.Option(
        False, "--pending", "-p", help="Show only pending tasks"
    ),
    completed: bool = typer.Option(
        False, "--completed", "-c", help="Show only completed tasks"
    ),
    priority: Optional[str] = typer.Option(
        None, "--priority", help="Filter by priority"
    ),
):
    """
    📋 [cyan]List[/cyan] all tasks.
    """
    service = get_service()
    tasks = service.get_all()
    
    # Apply filters
    if pending:
        tasks = [t for t in tasks if t.status == Status.PENDING]
    elif completed:
        tasks = [t for t in tasks if t.status == Status.COMPLETED]
    elif not all_tasks:
        # Default: show pending only
        tasks = [t for t in tasks if t.status == Status.PENDING]
    
    if priority:
        try:
            p = Priority(priority.lower())
            tasks = [t for t in tasks if t.priority == p]
        except ValueError:
            show_error_message(f"Invalid priority: {priority}")
    
    if not tasks:
        console.print(format_empty_state())
    else:
        console.print(format_task_table(tasks))
        console.print(f"\n[dim]Showing {len(tasks)} task(s)[/dim]")


@app.command()
def view(
    task_id: int = typer.Argument(..., help="Task ID to view"),
):
    """
    👁️ [cyan]View[/cyan] task details.
    """
    service = get_service()
    task = service.get_by_id(task_id)
    
    if task is None:
        show_error_message(f"Task #{task_id} not found")
        raise typer.Exit(1)
    
    console.print(format_single_task(task))


@app.command()
def complete(
    task_id: Optional[int] = typer.Argument(
        None, help="Task ID to complete"
    ),
    interactive: bool = typer.Option(
        True, "--interactive/--no-interactive", "-i", help="Use interactive selection"
    ),
):
    """
    ✅ Mark a task as [green]complete[/green].
    """
    service = get_service()
    
    if task_id is None and interactive:
        # Interactive selection
        tasks = service.get_pending()
        if not tasks:
            show_info_message("No pending tasks to complete!")
            raise typer.Exit()
        
        task_id = select_task_prompt(tasks, "complete")
        if task_id is None:
            raise typer.Exit()
    
    if task_id is None:
        show_error_message("Task ID is required")
        raise typer.Exit(1)
    
    task = service.complete(task_id)
    
    if task is None:
        show_error_message(f"Task #{task_id} not found")
        raise typer.Exit(1)
    
    show_completion_celebration(task.title)


@app.command()
def update(
    task_id: Optional[int] = typer.Argument(
        None, help="Task ID to update"
    ),
    title: Optional[str] = typer.Option(
        None, "--title", "-t", help="New title"
    ),
    description: Optional[str] = typer.Option(
        None, "--description", "-d", help="New description"
    ),
    priority: Optional[str] = typer.Option(
        None, "--priority", "-p", help="New priority"
    ),
    interactive: bool = typer.Option(
        True, "--interactive/--no-interactive", "-i", help="Use interactive prompts"
    ),
):
    """
    ✏️ [yellow]Update[/yellow] a task.
    """
    service = get_service()
    
    if task_id is None and interactive:
        tasks = service.get_all()
        if not tasks:
            show_info_message("No tasks to update!")
            raise typer.Exit()
        
        task_id = select_task_prompt(tasks, "update")
        if task_id is None:
            raise typer.Exit()
    
    if task_id is None:
        show_error_message("Task ID is required")
        raise typer.Exit(1)
    
    current_task = service.get_by_id(task_id)
    if current_task is None:
        show_error_message(f"Task #{task_id} not found")
        raise typer.Exit(1)
    
    if interactive and not any([title, description, priority]):
        updates = update_task_prompt(current_task)
        if not updates:
            show_warning_message("Update cancelled")
            raise typer.Exit()
    else:
        updates = {}
        if title:
            updates["title"] = title
        if description:
            updates["description"] = description
        if priority:
            updates["priority"] = Priority(priority.lower())
    
    task = service.update(task_id, **updates)
    show_success_message(f"Task #{task_id} updated")
    console.print(format_single_task(task))


@app.command()
def delete(
    task_id: Optional[int] = typer.Argument(
        None, help="Task ID to delete"
    ),
    force: bool = typer.Option(
        False, "--force", "-f", help="Skip confirmation"
    ),
    interactive: bool = typer.Option(
        True, "--interactive/--no-interactive", "-i", help="Use interactive selection"
    ),
):
    """
    🗑️ [red]Delete[/red] a task.
    """
    service = get_service()
    
    if task_id is None and interactive:
        tasks = service.get_all()
        if not tasks:
            show_info_message("No tasks to delete!")
            raise typer.Exit()
        
        task_id = select_task_prompt(tasks, "delete")
        if task_id is None:
            raise typer.Exit()
    
    if task_id is None:
        show_error_message("Task ID is required")
        raise typer.Exit(1)
    
    task = service.get_by_id(task_id)
    if task is None:
        show_error_message(f"Task #{task_id} not found")
        raise typer.Exit(1)
    
    if not force:
        if not confirm_delete(task.title):
            show_warning_message("Delete cancelled")
            raise typer.Exit()
    
    service.delete(task_id)
    show_success_message(f"Task #{task_id} deleted")


@app.command()
def search(
    query: Optional[str] = typer.Argument(
        None, help="Search query"
    ),
    interactive: bool = typer.Option(
        True, "--interactive/--no-interactive", "-i", help="Use interactive prompt"
    ),
):
    """
    🔍 [magenta]Search[/magenta] tasks by keyword.
    """
    service = get_service()
    
    if query is None and interactive:
        query = search_prompt()
        if not query:
            raise typer.Exit()
    
    if not query:
        show_error_message("Search query is required")
        raise typer.Exit(1)
    
    tasks = service.get_all()
    
    # Simple search in title and description
    query_lower = query.lower()
    results = [
        t for t in tasks
        if query_lower in t.title.lower() or 
           (t.description and query_lower in t.description.lower()) or
           any(query_lower in tag for tag in t.tags)
    ]
    
    if not results:
        show_info_message(f"No tasks found matching '{query}'")
    else:
        console.print(f"\n[cyan]Search results for '[bold]{query}[/bold]':[/cyan]\n")
        console.print(format_task_table(results))
        console.print(f"\n[dim]Found {len(results)} task(s)[/dim]")


@app.command()
def filter():
    """
    🎯 [yellow]Filter[/yellow] tasks by criteria.
    """
    service = get_service()
    
    criteria = filter_prompt()
    tasks = service.get_all()
    
    # Apply filters
    if "priorities" in criteria:
        tasks = [t for t in tasks if t.priority in criteria["priorities"]]
    
    if "status" in criteria:
        tasks = [t for t in tasks if t.status == criteria["status"]]
    
    if "tags" in criteria:
        filter_tags = criteria["tags"]
        tasks = [
            t for t in tasks 
            if any(tag in t.tags for tag in filter_tags)
        ]
    
    if not tasks:
        console.print(format_empty_state("No tasks match the filter"))
    else:
        console.print(format_task_table(tasks))
        console.print(f"\n[dim]Found {len(tasks)} task(s)[/dim]")


@app.command()
def stats():
    """
    📊 Show task [cyan]statistics[/cyan].
    """
    service = get_service()
    stats_data = service.get_statistics()
    console.print(format_stats_panel(stats_data))


# Cleanup on exit
import atexit
atexit.register(close_database)


if __name__ == "__main__":
    app()
