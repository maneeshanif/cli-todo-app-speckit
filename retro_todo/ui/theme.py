"""
Cyberpunk color theme and Questionary styling for Retro Todo.

T028, T029: Theme constants and retro style configuration.
"""
from questionary import Style


# Cyberpunk Color Palette (Constitutional)
class COLORS:
    """Retro cyberpunk color constants for terminal display."""
    
    # Primary accent colors
    CYAN = "#00FFFF"
    MAGENTA = "#FF00FF"
    GREEN = "#00FF00"
    YELLOW = "#FFFF00"
    RED = "#FF0000"
    
    # Secondary colors
    ORANGE = "#FFA500"
    PURPLE = "#8B00FF"
    PINK = "#FF69B4"
    
    # Neutral colors
    WHITE = "#FFFFFF"
    BLACK = "#000000"
    GRAY = "#808080"
    DIM = "#666666"
    
    # Rich style names
    RICH_CYAN = "cyan"
    RICH_MAGENTA = "magenta"
    RICH_GREEN = "green"
    RICH_YELLOW = "yellow"
    RICH_RED = "red"
    RICH_ORANGE = "orange1"


# Questionary Retro Style
retro_style = Style([
    ('qmark', f'fg:{COLORS.CYAN} bold'),           # Cyan question mark
    ('question', f'fg:{COLORS.MAGENTA} bold'),     # Magenta question text
    ('answer', f'fg:{COLORS.GREEN}'),              # Green user answer
    ('pointer', f'fg:{COLORS.CYAN} bold'),         # Cyan selection pointer
    ('highlighted', f'fg:{COLORS.MAGENTA} bold'),  # Magenta highlighted option
    ('selected', f'fg:{COLORS.GREEN}'),            # Green selected item
    ('separator', f'fg:{COLORS.YELLOW}'),          # Yellow separator lines
    ('instruction', f'fg:{COLORS.CYAN}'),          # Cyan instructions
    ('text', f'fg:{COLORS.WHITE}'),                # White normal text
    ('disabled', f'fg:{COLORS.DIM}'),              # Dim disabled items
])


# Rich Theme Configuration
RICH_THEME = {
    "info": "cyan",
    "warning": "yellow",
    "error": "red bold",
    "success": "green bold",
    "highlight": "magenta bold",
    "primary": "cyan",
    "secondary": "magenta",
}


# ASCII Art Color Schemes
SPLASH_COLORS = {
    "title": "cyan",
    "subtitle": "magenta",
    "credit": "green",
    "border": "cyan",
    "decoration": "yellow",
}
