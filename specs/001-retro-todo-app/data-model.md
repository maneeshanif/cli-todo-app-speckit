# Data Model: Retro Terminal Todo Manager

**Feature**: 001-retro-todo-app  
**Date**: 2025-12-07  
**Phase**: 1 (Design)

## Overview

This document defines all Pydantic v2 data models, enumerations, and relationships for the todo management system. All models follow constitution principles IV (Pydantic v2) and enforce validation at the data layer.

---

## Enumerations

### Priority (Enum)

Represents task importance level with corresponding visual indicators.

```python
from enum import Enum

class Priority(str, Enum):
    """Task priority levels with visual color coding."""
    
    LOW = "low"          # 🟢 Green
    MEDIUM = "medium"    # 🟡 Yellow
    HIGH = "high"        # 🟠 Orange
    URGENT = "urgent"    # 🔴 Red
    
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
```

**Design Rationale**: String-based enum for JSON serialization compatibility with TinyDB. Color/icon properties enable consistent UI rendering.

---

### Status (Enum)

Represents task completion state.

```python
class Status(str, Enum):
    """Task completion status."""
    
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
```

**Design Rationale**: Two-state system keeps MVP simple. Future extension could add ARCHIVED, BLOCKED states in Phase II.

---

### RecurrencePattern (Enum)

Defines task repetition schedule.

```python
class RecurrencePattern(str, Enum):
    """Task recurrence frequency."""
    
    NONE = "none"        # One-time task
    DAILY = "daily"      # Repeats every day
    WEEKLY = "weekly"    # Repeats every 7 days
    MONTHLY = "monthly"  # Repeats every 30 days (approximation)
    
    @property
    def icon(self) -> str:
        """Recurrence indicator."""
        return "🔁" if self != RecurrencePattern.NONE else ""
    
    @property
    def display_label(self) -> str:
        """Human-readable label for UI."""
        if self == RecurrencePattern.NONE:
            return ""
        return f"🔁 {self.value.capitalize()}"
```

**Design Rationale**: String-based for JSON compatibility. Monthly uses 30-day approximation (acceptable per spec assumptions). Icon property enables consistent badge rendering.

---

## TodoTask Model

Primary data entity representing a single task.

```python
from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import Optional

class TodoTask(BaseModel):
    """
    A single task in the todo system.
    
    Attributes:
        id: Unique task identifier (auto-generated)
        title: Task name (required, 1-500 characters)
        description: Optional detailed description
        status: Completion state (pending/completed)
        priority: Importance level (low/medium/high/urgent)
        tags: Categorization labels (comma-separated list)
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
    
    # Validation rules
    
    @field_validator('title')
    @classmethod
    def title_not_empty(cls, v: str) -> str:
        """Ensure title contains non-whitespace characters."""
        if not v.strip():
            raise ValueError('Title cannot be empty or only whitespace')
        return v.strip()
    
    @field_validator('due_date')
    @classmethod
    def due_date_future_or_none(cls, v: Optional[datetime]) -> Optional[datetime]:
        """Validate due date is not in the past (if set)."""
        if v and v < datetime.now():
            raise ValueError('Due date cannot be in the past')
        return v
    
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
        # Parse datetime strings back to datetime objects
        for field in ['due_date', 'created_at', 'updated_at', 'completed_at']:
            if data.get(field):
                data[field] = datetime.fromisoformat(data[field])
        
        # Convert enum strings back to enum instances
        data['status'] = Status(data['status'])
        data['priority'] = Priority(data['priority'])
        data['recurrence_pattern'] = RecurrencePattern(data['recurrence_pattern'])
        
        return cls(**data)
    
    # Rich display helpers
    
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
```

**Design Rationale**:
- Pydantic v2 syntax with `@field_validator` (not v1 `@validator`)
- Strict type hints on all fields for IDE support and runtime validation
- Business logic methods (`mark_complete`, `is_overdue`) encapsulate behavior
- Rich formatting methods enable consistent UI rendering across all screens
- `to_dict`/`from_dict` handle TinyDB serialization (datetime → ISO strings)

---

## Entity Relationships

### TodoTask ↔ TinyDB Document

One-to-one mapping between TodoTask instances and TinyDB JSON documents.

```
TodoTask (Python Object)
    ↓ serialization via to_dict()
TinyDB Document (JSON)
    ↓ deserialization via from_dict()
TodoTask (Python Object)
```

**Storage Format** (TinyDB JSON):
```json
{
  "_default": {
    "1": {
      "id": 1,
      "title": "Fix login bug",
      "description": "Users cannot login with Google OAuth",
      "status": "pending",
      "priority": "urgent",
      "tags": ["backend", "bug", "security"],
      "due_date": "2025-12-08T14:00:00",
      "recurrence_pattern": "none",
      "created_at": "2025-12-07T10:30:00",
      "updated_at": "2025-12-07T10:30:00",
      "completed_at": null
    }
  }
}
```

---

## Validation Rules Summary

| Field | Validation | Error Message |
|-------|------------|---------------|
| title | Non-empty after strip() | "Title cannot be empty or only whitespace" |
| title | Length 1-500 | Pydantic automatic (FieldValidationError) |
| description | Length ≤5000 | Pydantic automatic |
| due_date | Future or None | "Due date cannot be in the past" |
| tags | Lowercase, stripped, deduplicated | Automatic normalization (no error) |
| priority | Valid enum value | Pydantic automatic (ValueError) |
| status | Valid enum value | Pydantic automatic (ValueError) |
| recurrence_pattern | Valid enum value | Pydantic automatic (ValueError) |

---

## Database Schema Considerations

### TinyDB Table Structure

```python
# Database initialization
db = TinyDB('todo_data.json', storage=CachingMiddleware(JSONStorage))
tasks_table = db.table('tasks')

# Index strategy (performance optimization)
# TinyDB doesn't support indexes natively, but CachingMiddleware provides in-memory speedup
# For searches, iterate through cached results (acceptable for <100k tasks per spec)
```

### ID Generation Strategy

```python
# Atomic ID generation to prevent collisions
def generate_task_id() -> int:
    """Generate next available task ID."""
    all_tasks = tasks_table.all()
    if not all_tasks:
        return 1
    return max(task['id'] for task in all_tasks) + 1
```

**Design Rationale**: Simple auto-increment strategy acceptable for single-user application. No UUID needed (no distributed system requirements).

---

## Migration Strategy

**Phase I**: No migrations needed (greenfield project).

**Future Phases**: If schema changes required:
1. Add version field to TodoTask model
2. Create migration functions: `migrate_v1_to_v2(task_dict: dict) -> dict`
3. Run migrations on app startup before loading data

---

## Testing Considerations

### Model Validation Tests

```python
# Example test cases for TodoTask validation

def test_title_cannot_be_empty():
    with pytest.raises(ValueError, match="Title cannot be empty"):
        TodoTask(id=1, title="   ")

def test_due_date_cannot_be_past():
    past_date = datetime.now() - timedelta(days=1)
    with pytest.raises(ValueError, match="Due date cannot be in the past"):
        TodoTask(id=1, title="Task", due_date=past_date)

def test_tags_are_normalized():
    task = TodoTask(id=1, title="Task", tags=["BACKEND", " frontend ", "backend"])
    assert task.tags == ["backend", "frontend"]  # Lowercase, stripped, deduplicated
```

---

## Conclusion

All data models defined with strict Pydantic v2 validation, comprehensive business logic methods, and Rich formatting helpers. Schema supports all 37 functional requirements from specification.

**Next Phase**: Generate CLI command contracts and quickstart guide.
