"""
TodoTask Pydantic v2 model for task management.

Primary data entity representing a single task with validation,
business logic, and serialization methods.

T017, T019, T021: GREEN phase implementation.
"""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, field_validator

from .enums import Priority, Status, RecurrencePattern


class TodoTask(BaseModel):
    """
    A single task in the todo system.
    
    Attributes:
        id: Unique task identifier (auto-generated)
        title: Task name (required, 1-500 characters)
        description: Optional detailed description
        status: Completion state (pending/completed)
        priority: Importance level (low/medium/high/urgent)
        tags: Categorization labels
        due_date: Optional deadline with time component
        recurrence_pattern: Repetition schedule
        created_at: Task creation timestamp
        updated_at: Last modification timestamp
        completed_at: Completion timestamp (null if pending)
    """
    
    # Primary fields
    id: int = Field(description="Unique task identifier")
    title: str = Field(min_length=1, max_length=500, description="Task title")
    description: Optional[str] = Field(default=None, max_length=5000)
    
    # State fields
    status: Status = Field(default=Status.PENDING)
    priority: Priority = Field(default=Priority.MEDIUM)
    
    # Organization fields
    tags: list[str] = Field(default_factory=list, description="Categorization tags")
    
    # Time fields
    due_date: Optional[datetime] = Field(default=None)
    recurrence_pattern: RecurrencePattern = Field(default=RecurrencePattern.NONE)
    
    # Audit fields
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    completed_at: Optional[datetime] = Field(default=None)
    
    # Pydantic v2 configuration
    model_config = {
        "validate_assignment": True,
        "str_strip_whitespace": True,
    }
    
    # Validation rules using Pydantic v2 syntax
    
    @field_validator('title')
    @classmethod
    def title_not_empty(cls, v: str) -> str:
        """Ensure title contains non-whitespace characters."""
        if not v.strip():
            raise ValueError('Title cannot be empty or only whitespace')
        return v.strip()
    
    @field_validator('tags')
    @classmethod
    def normalize_tags(cls, v: list[str]) -> list[str]:
        """Normalize tags: lowercase, strip whitespace, deduplicate."""
        normalized = [tag.strip().lower() for tag in v if tag.strip()]
        return list(dict.fromkeys(normalized))  # Deduplicate while preserving order
    
    # Business logic methods
    
    def mark_complete(self) -> None:
        """Mark task as completed and set completion timestamp."""
        self.status = Status.COMPLETED
        self.completed_at = datetime.now()
        self.updated_at = datetime.now()
    
    def is_overdue(self) -> bool:
        """Check if task is past due date and still pending."""
        return (
            self.status == Status.PENDING 
            and self.due_date is not None 
            and self.due_date < datetime.now()
        )
    
    def has_recurrence(self) -> bool:
        """Check if task repeats."""
        return self.recurrence_pattern != RecurrencePattern.NONE
    
    # Serialization methods for TinyDB compatibility
    
    def to_dict(self) -> dict:
        """Convert to dictionary for TinyDB storage."""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'status': self.status.value,
            'priority': self.priority.value,
            'tags': self.tags,
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'recurrence_pattern': self.recurrence_pattern.value,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'TodoTask':
        """Create instance from TinyDB dictionary."""
        # Create a copy to avoid modifying original
        data = data.copy()
        
        # Parse datetime strings back to datetime objects
        for field in ['due_date', 'created_at', 'updated_at', 'completed_at']:
            if data.get(field):
                data[field] = datetime.fromisoformat(data[field])
        
        # Convert enum strings back to enum instances
        data['status'] = Status(data['status'])
        data['priority'] = Priority(data['priority'])
        data['recurrence_pattern'] = RecurrencePattern(data['recurrence_pattern'])
        
        return cls(**data)
    
    # Rich display helper methods
    
    def format_priority_badge(self) -> str:
        """Rich markup for priority display."""
        return f"[{self.priority.color}]{self.priority.icon} {self.priority.value.upper()}[/{self.priority.color}]"
    
    def format_status_badge(self) -> str:
        """Rich markup for status display."""
        style = "green" if self.status == Status.COMPLETED else "yellow"
        return f"[{style}]{self.status.icon} {self.status.value.capitalize()}[/{style}]"
    
    def format_tags_display(self) -> str:
        """Rich markup for tags display."""
        if not self.tags:
            return "[dim]No tags[/dim]"
        return " ".join([f"[cyan]#{tag}[/cyan]" for tag in self.tags])
    
    def format_due_date_display(self) -> str:
        """Rich markup for due date with countdown/overdue warning."""
        if not self.due_date:
            return "[dim]No due date[/dim]"
        
        now = datetime.now()
        delta = self.due_date - now
        
        if delta.total_seconds() < 0:
            # Overdue
            return f"[red]⚠️ OVERDUE: {self.due_date.strftime('%Y-%m-%d %H:%M')}[/red]"
        elif delta.total_seconds() < 86400:  # Less than 24 hours
            hours = int(delta.total_seconds() / 3600)
            return f"[yellow]⏰ {hours}h remaining[/yellow]"
        else:
            return f"[green]📅 {self.due_date.strftime('%Y-%m-%d %H:%M')}[/green]"
