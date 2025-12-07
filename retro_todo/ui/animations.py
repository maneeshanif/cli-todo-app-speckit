"""
Animation effects for Retro Todo.

Provides completion celebrations and loading spinners.

T128, T129: Polish phase implementation.
"""
import time
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.panel import Panel
from rich.text import Text

console = Console()


def show_completion_celebration(task_title: str) -> None:
    """
    Display a celebration animation when task is completed.
    
    Args:
        task_title: Title of completed task
    """
    # Create celebration text
    celebration = Text()
    celebration.append("\n")
    celebration.append("🎉 ", style="yellow")
    celebration.append("TASK COMPLETED!", style="bold green")
    celebration.append(" 🎉\n\n", style="yellow")
    celebration.append(f"✅ {task_title}\n", style="green")
    celebration.append("\n")
    celebration.append("🌟 ", style="yellow")
    celebration.append("Great job!", style="cyan")
    celebration.append(" 🌟", style="yellow")
    
    panel = Panel(
        celebration,
        border_style="green",
        padding=(1, 4),
    )
    
    console.print()
    console.print(panel)
    console.print()


def show_loading_spinner(message: str = "Loading..."):
    """
    Create a loading spinner context manager.
    
    Args:
        message: Message to display while loading
        
    Returns:
        Progress context manager
    """
    return Progress(
        SpinnerColumn(style="cyan"),
        TextColumn("[cyan]{task.description}[/cyan]"),
        console=console,
        transient=True,
    )


def show_success_message(message: str) -> None:
    """Display a success message."""
    console.print(f"[green]✅ {message}[/green]")


def show_error_message(message: str) -> None:
    """Display an error message."""
    console.print(f"[red]❌ {message}[/red]")


def show_warning_message(message: str) -> None:
    """Display a warning message."""
    console.print(f"[yellow]⚠️ {message}[/yellow]")


def show_info_message(message: str) -> None:
    """Display an info message."""
    console.print(f"[cyan]ℹ️ {message}[/cyan]")
