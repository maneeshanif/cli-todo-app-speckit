"""
PyFiglet ASCII art splash screen for Retro Todo.

Displays the application banner with developer credit.

T031: GREEN phase implementation.
"""
import pyfiglet
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.align import Align

from .theme import SPLASH_COLORS, COLORS

console = Console()


def get_splash_text() -> str:
    """
    Generate ASCII art banner text using PyFiglet.
    
    Returns:
        ASCII art string for "TODO"
    """
    return pyfiglet.figlet_format("RETRO TODO", font="slant")


def show_splash() -> None:
    """
    Display the retro splash screen with cyberpunk styling.
    
    Includes:
    - ASCII art banner
    - Application title
    - Version information
    - Developer credit (maneeshanif)
    """
    # Generate ASCII art
    ascii_art = get_splash_text()
    
    # Create styled text
    art_text = Text(ascii_art, style="cyan bold")
    
    # Build the splash content
    content = Text()
    content.append("\n")
    content.append(ascii_art, style="cyan bold")
    content.append("\n")
    content.append("═" * 50, style="magenta")
    content.append("\n\n")
    content.append("🎮 ", style="yellow")
    content.append("TERMINAL TASK MANAGER", style="magenta bold")
    content.append(" 🎮", style="yellow")
    content.append("\n\n")
    content.append("Version: ", style="dim")
    content.append("0.1.0", style="green")
    content.append("\n\n")
    content.append("━" * 50, style="cyan dim")
    content.append("\n")
    
    # Create panel with developer credit in subtitle
    panel = Panel(
        Align.center(content),
        title="[bold cyan]🕹️  RETRO TODO  🕹️[/bold cyan]",
        subtitle="[bold green]Developer by: maneeshanif[/bold green]",
        border_style="cyan",
        padding=(1, 4),
    )
    
    console.print()
    console.print(panel)
    console.print()


def show_welcome_message() -> None:
    """Display a welcome message after splash."""
    console.print()
    console.print("[cyan]Welcome to Retro Todo![/cyan]", justify="center")
    console.print("[dim]Type [green]retro-todo --help[/green] for available commands[/dim]", justify="center")
    console.print()


def show_goodbye_message() -> None:
    """Display exit message."""
    console.print()
    console.print("[magenta]Thanks for using Retro Todo![/magenta]", justify="center")
    console.print("[cyan]See you next time! 🎮[/cyan]", justify="center")
    console.print()
