"""
Retro Todo - Interactive App Mode

Single entry point with main menu loop.
"""
import questionary
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

from retro_todo import __version__
from retro_todo.database.db import init_database, close_database
from retro_todo.services.todo_service import TodoService
from retro_todo.models.enums import Priority, Status
from retro_todo.ui.splash import show_splash
from retro_todo.ui.tables import (
    format_task_table, 
    format_stats_panel, 
    format_empty_state,
    format_single_task,
)
from retro_todo.ui.prompts import add_task_prompt, confirm_delete
from retro_todo.ui.animations import (
    show_completion_celebration,
    show_success_message,
    show_error_message,
    show_warning_message,
    show_info_message
)
from retro_todo.ui.theme import retro_style, COLORS

console = Console()


def get_service() -> TodoService:
    """Get or initialize todo service."""
    init_database()
    return TodoService()


def show_main_menu() -> str:
    """Display main menu and get user choice."""
    choices = [
        "📋  View All Tasks",
        "➕  Add New Task",
        "✅  Complete a Task",
        "✏️   Edit a Task",
        "🗑️   Delete a Task",
        "🔍  Search Tasks",
        "📊  View Statistics",
        "─────────────────",
        "🚪  Exit",
    ]
    
    return questionary.select(
        "What would you like to do?",
        choices=choices,
        style=retro_style,
        instruction="(Use ↑↓ arrows, Enter to select)"
    ).ask()


def view_all_tasks(service: TodoService):
    """Display all tasks."""
    console.print()
    tasks = service.get_all()
    
    if not tasks:
        console.print(format_empty_state())
    else:
        # Show filter options
        filter_choice = questionary.select(
            "Filter tasks:",
            choices=[
                "📋 All Tasks",
                "⏳ Pending Only", 
                "✅ Completed Only",
                "🔴 Urgent Priority",
                "🟠 High Priority",
                "🟡 Medium Priority",
                "🟢 Low Priority",
            ],
            style=retro_style
        ).ask()
        
        if filter_choice is None:
            return
            
        filtered_tasks = tasks
        
        if "Pending" in filter_choice:
            filtered_tasks = [t for t in tasks if t.status == Status.PENDING]
        elif "Completed" in filter_choice:
            filtered_tasks = [t for t in tasks if t.status == Status.COMPLETED]
        elif "Urgent" in filter_choice:
            filtered_tasks = [t for t in tasks if t.priority == Priority.URGENT]
        elif "High" in filter_choice:
            filtered_tasks = [t for t in tasks if t.priority == Priority.HIGH]
        elif "Medium" in filter_choice:
            filtered_tasks = [t for t in tasks if t.priority == Priority.MEDIUM]
        elif "Low" in filter_choice:
            filtered_tasks = [t for t in tasks if t.priority == Priority.LOW]
        
        if not filtered_tasks:
            show_info_message("No tasks match this filter")
        else:
            console.print(format_task_table(filtered_tasks))
            console.print(f"\n[dim]Showing {len(filtered_tasks)} of {len(tasks)} task(s)[/dim]")
    
    console.print()
    questionary.press_any_key_to_continue(
        "Press any key to continue...",
        style=retro_style
    ).ask()


def add_new_task(service: TodoService):
    """Add a new task interactively."""
    console.print()
    console.print(Panel(
        "[cyan]➕ ADD NEW TASK[/cyan]",
        border_style="cyan",
        padding=(0, 2)
    ))
    console.print()
    
    task_data = add_task_prompt()
    
    if task_data is None:
        show_warning_message("Task creation cancelled")
        return
    
    task = service.create(**task_data)
    show_success_message(f"Task #{task.id} created: {task.title}")
    console.print(format_single_task(task))
    
    console.print()
    questionary.press_any_key_to_continue(
        "Press any key to continue...",
        style=retro_style
    ).ask()


def complete_task(service: TodoService):
    """Mark a task as complete."""
    console.print()
    tasks = [t for t in service.get_all() if t.status == Status.PENDING]
    
    if not tasks:
        show_info_message("No pending tasks to complete! 🎉")
        questionary.press_any_key_to_continue(
            "Press any key to continue...",
            style=retro_style
        ).ask()
        return
    
    # Create choices with task info
    choices = [
        f"#{t.id} | {t.priority.icon} {t.title[:40]}" 
        for t in tasks
    ]
    choices.append("← Back to menu")
    
    console.print(Panel(
        "[green]✅ COMPLETE A TASK[/green]",
        border_style="green",
        padding=(0, 2)
    ))
    console.print()
    
    selected = questionary.select(
        "Select task to complete:",
        choices=choices,
        style=retro_style
    ).ask()
    
    if selected is None or "Back" in selected:
        return
    
    # Extract task ID
    task_id = int(selected.split("|")[0].strip().replace("#", ""))
    task = service.complete(task_id)
    
    if task:
        show_completion_celebration(task.title)
    else:
        show_error_message("Task not found")
    
    questionary.press_any_key_to_continue(
        "Press any key to continue...",
        style=retro_style
    ).ask()


def edit_task(service: TodoService):
    """Edit an existing task."""
    console.print()
    tasks = service.get_all()
    
    if not tasks:
        show_info_message("No tasks to edit")
        questionary.press_any_key_to_continue(
            "Press any key to continue...",
            style=retro_style
        ).ask()
        return
    
    # Create choices with task info
    choices = [
        f"#{t.id} | {t.priority.icon} {t.status.icon} {t.title[:35]}" 
        for t in tasks
    ]
    choices.append("← Back to menu")
    
    console.print(Panel(
        "[yellow]✏️ EDIT A TASK[/yellow]",
        border_style="yellow",
        padding=(0, 2)
    ))
    console.print()
    
    selected = questionary.select(
        "Select task to edit:",
        choices=choices,
        style=retro_style
    ).ask()
    
    if selected is None or "Back" in selected:
        return
    
    # Extract task ID
    task_id = int(selected.split("|")[0].strip().replace("#", ""))
    task = service.get_by_id(task_id)
    
    if not task:
        show_error_message("Task not found")
        return
    
    # Show current task
    console.print(format_single_task(task))
    console.print()
    
    # What to edit?
    edit_choice = questionary.select(
        "What would you like to edit?",
        choices=[
            "📝 Title",
            "📄 Description", 
            "🎯 Priority",
            "🏷️  Tags",
            "← Back to menu"
        ],
        style=retro_style
    ).ask()
    
    if edit_choice is None or "Back" in edit_choice:
        return
    
    updates = {}
    
    if "Title" in edit_choice:
        new_title = questionary.text(
            "New title:",
            default=task.title,
            style=retro_style
        ).ask()
        if new_title:
            updates["title"] = new_title
            
    elif "Description" in edit_choice:
        new_desc = questionary.text(
            "New description:",
            default=task.description or "",
            style=retro_style
        ).ask()
        updates["description"] = new_desc
        
    elif "Priority" in edit_choice:
        new_priority = questionary.select(
            "New priority:",
            choices=[
                "🟢 Low",
                "🟡 Medium",
                "🟠 High",
                "🔴 Urgent"
            ],
            style=retro_style
        ).ask()
        if new_priority:
            priority_map = {
                "🟢 Low": Priority.LOW,
                "🟡 Medium": Priority.MEDIUM,
                "🟠 High": Priority.HIGH,
                "🔴 Urgent": Priority.URGENT
            }
            updates["priority"] = priority_map[new_priority]
            
    elif "Tags" in edit_choice:
        current_tags = ", ".join(task.tags) if task.tags else ""
        new_tags = questionary.text(
            "Tags (comma-separated):",
            default=current_tags,
            style=retro_style
        ).ask()
        if new_tags is not None:
            updates["tags"] = [t.strip() for t in new_tags.split(",") if t.strip()]
    
    if updates:
        updated_task = service.update(task_id, **updates)
        if updated_task:
            show_success_message(f"Task #{task_id} updated!")
            console.print(format_single_task(updated_task))
        else:
            show_error_message("Failed to update task")
    
    console.print()
    questionary.press_any_key_to_continue(
        "Press any key to continue...",
        style=retro_style
    ).ask()


def delete_task(service: TodoService):
    """Delete a task."""
    console.print()
    tasks = service.get_all()
    
    if not tasks:
        show_info_message("No tasks to delete")
        questionary.press_any_key_to_continue(
            "Press any key to continue...",
            style=retro_style
        ).ask()
        return
    
    # Create choices with task info
    choices = [
        f"#{t.id} | {t.priority.icon} {t.status.icon} {t.title[:35]}" 
        for t in tasks
    ]
    choices.append("← Back to menu")
    
    console.print(Panel(
        "[red]🗑️ DELETE A TASK[/red]",
        border_style="red",
        padding=(0, 2)
    ))
    console.print()
    
    selected = questionary.select(
        "Select task to delete:",
        choices=choices,
        style=retro_style
    ).ask()
    
    if selected is None or "Back" in selected:
        return
    
    # Extract task ID and title
    task_id = int(selected.split("|")[0].strip().replace("#", ""))
    task = service.get_by_id(task_id)
    
    if not task:
        show_error_message("Task not found")
        return
    
    # Confirm deletion
    if confirm_delete(task.title):
        if service.delete(task_id):
            show_success_message(f"Task #{task_id} deleted")
        else:
            show_error_message("Failed to delete task")
    else:
        show_info_message("Deletion cancelled")
    
    console.print()
    questionary.press_any_key_to_continue(
        "Press any key to continue...",
        style=retro_style
    ).ask()


def search_tasks(service: TodoService):
    """Search for tasks."""
    console.print()
    console.print(Panel(
        "[magenta]🔍 SEARCH TASKS[/magenta]",
        border_style="magenta",
        padding=(0, 2)
    ))
    console.print()
    
    query = questionary.text(
        "Enter search term:",
        style=retro_style
    ).ask()
    
    if not query:
        return
    
    tasks = service.get_all()
    query_lower = query.lower()
    
    # Search in title, description, and tags
    results = [
        t for t in tasks
        if query_lower in t.title.lower()
        or (t.description and query_lower in t.description.lower())
        or any(query_lower in tag.lower() for tag in t.tags)
    ]
    
    console.print()
    if results:
        console.print(f"[green]Found {len(results)} result(s) for '{query}':[/green]")
        console.print()
        console.print(format_task_table(results))
    else:
        show_info_message(f"No tasks found matching '{query}'")
    
    console.print()
    questionary.press_any_key_to_continue(
        "Press any key to continue...",
        style=retro_style
    ).ask()


def view_statistics(service: TodoService):
    """Display task statistics."""
    console.print()
    stats = service.get_statistics()
    console.print(format_stats_panel(stats))
    
    console.print()
    questionary.press_any_key_to_continue(
        "Press any key to continue...",
        style=retro_style
    ).ask()


def show_goodbye():
    """Show exit message."""
    console.print()
    goodbye = Text()
    goodbye.append("\n")
    goodbye.append("  👋 ", style="yellow")
    goodbye.append("Thanks for using ", style="white")
    goodbye.append("RETRO TODO", style="bold cyan")
    goodbye.append("!", style="white")
    goodbye.append("\n\n")
    goodbye.append("  🎮 ", style="magenta")
    goodbye.append("Keep crushing those tasks!", style="green")
    goodbye.append(" 🎮\n", style="magenta")
    goodbye.append("\n")
    goodbye.append("  Developer by: ", style="dim")
    goodbye.append("maneeshanif", style="cyan")
    goodbye.append("\n")
    
    console.print(Panel(
        goodbye,
        border_style="cyan",
        padding=(0, 2)
    ))
    console.print()


def run_interactive():
    """Main interactive loop."""
    # Show splash on start
    show_splash()
    
    # Initialize service
    service = get_service()
    
    # Main loop
    running = True
    while running:
        console.print()
        choice = show_main_menu()
        
        if choice is None or "Exit" in choice:
            running = False
        elif "View All" in choice:
            view_all_tasks(service)
        elif "Add New" in choice:
            add_new_task(service)
        elif "Complete" in choice:
            complete_task(service)
        elif "Edit" in choice:
            edit_task(service)
        elif "Delete" in choice:
            delete_task(service)
        elif "Search" in choice:
            search_tasks(service)
        elif "Statistics" in choice:
            view_statistics(service)
    
    # Goodbye message
    show_goodbye()
    
    # Cleanup
    close_database()


def main():
    """Entry point for the interactive app."""
    try:
        run_interactive()
    except KeyboardInterrupt:
        console.print("\n")
        show_goodbye()


if __name__ == "__main__":
    main()
