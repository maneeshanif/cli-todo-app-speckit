"""
Enumeration types for Retro Todo task management.

Defines Priority, Status, and RecurrencePattern enums with visual properties
for terminal display using Rich library.

T011, T013, T015: GREEN phase implementation.
"""
from enum import Enum


class Priority(str, Enum):
    """
    Task priority levels with visual color coding.
    
    Inherits from str for JSON serialization compatibility with TinyDB.
    """
    
    LOW = "low"          # 🟢 Green - Low urgency
    MEDIUM = "medium"    # 🟡 Yellow - Normal priority
    HIGH = "high"        # 🟠 Orange - Important
    URGENT = "urgent"    # 🔴 Red - Critical
    
    @property
    def color(self) -> str:
        """Rich color style for terminal display."""
        color_map = {
            Priority.LOW: "green",
            Priority.MEDIUM: "yellow",
            Priority.HIGH: "orange1",
            Priority.URGENT: "red"
        }
        return color_map[self]
    
    @property
    def icon(self) -> str:
        """Emoji indicator for quick visual identification."""
        icon_map = {
            Priority.LOW: "🟢",
            Priority.MEDIUM: "🟡",
            Priority.HIGH: "🟠",
            Priority.URGENT: "🔴"
        }
        return icon_map[self]


class Status(str, Enum):
    """
    Task completion status.
    
    Two-state system for MVP. Future extension could add ARCHIVED, BLOCKED.
    """
    
    PENDING = "pending"      # ⏳ In progress
    COMPLETED = "completed"  # ✅ Done
    
    @property
    def icon(self) -> str:
        """Status indicator icon."""
        return "⏳" if self == Status.PENDING else "✅"
    
    @property
    def display_style(self) -> str:
        """Rich text styling for task display."""
        # Completed tasks use strikethrough + dim
        return "strike dim" if self == Status.COMPLETED else ""


class RecurrencePattern(str, Enum):
    """
    Task recurrence frequency.
    
    Monthly uses 30-day approximation (acceptable per spec assumptions).
    """
    
    NONE = "none"        # One-time task
    DAILY = "daily"      # Repeats every day
    WEEKLY = "weekly"    # Repeats every 7 days
    MONTHLY = "monthly"  # Repeats every 30 days (approximation)
    
    @property
    def icon(self) -> str:
        """Recurrence indicator icon."""
        return "🔁" if self != RecurrencePattern.NONE else ""
    
    @property
    def display_label(self) -> str:
        """Human-readable label for UI."""
        if self == RecurrencePattern.NONE:
            return ""
        return f"🔁 {self.value.capitalize()}"
