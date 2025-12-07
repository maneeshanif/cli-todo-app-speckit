"""
Unit tests for TodoTask Pydantic model.

Tests T016, T018, T020: RED phase tests for model validation, business logic, serialization.
"""
import pytest
from datetime import datetime, timedelta
from pydantic import ValidationError
from retro_todo.models.todo import TodoTask
from retro_todo.models.enums import Priority, Status, RecurrencePattern


class TestTodoTaskValidation:
    """Tests for TodoTask validation - T016."""
    
    def test_create_task_with_required_fields(self):
        """Can create task with just id and title."""
        task = TodoTask(id=1, title="Test task")
        assert task.id == 1
        assert task.title == "Test task"
        assert task.status == Status.PENDING
        assert task.priority == Priority.MEDIUM
    
    def test_title_cannot_be_empty(self):
        """Title validation rejects empty strings."""
        with pytest.raises(ValidationError):
            TodoTask(id=1, title="")
    
    def test_title_cannot_be_whitespace_only(self):
        """Title validation rejects whitespace-only strings."""
        with pytest.raises(ValidationError):
            TodoTask(id=1, title="   ")
    
    def test_title_is_stripped(self):
        """Title whitespace is trimmed."""
        task = TodoTask(id=1, title="  Test task  ")
        assert task.title == "Test task"
    
    def test_due_date_can_be_future(self):
        """Due date accepts future dates."""
        future_date = datetime.now() + timedelta(days=1)
        task = TodoTask(id=1, title="Test", due_date=future_date)
        assert task.due_date == future_date
    
    def test_due_date_can_be_none(self):
        """Due date can be omitted."""
        task = TodoTask(id=1, title="Test")
        assert task.due_date is None
    
    def test_tags_are_normalized(self):
        """Tags are lowercased and stripped."""
        task = TodoTask(id=1, title="Test", tags=["BACKEND", " Frontend ", "API"])
        assert task.tags == ["backend", "frontend", "api"]
    
    def test_tags_are_deduplicated(self):
        """Duplicate tags are removed."""
        task = TodoTask(id=1, title="Test", tags=["backend", "BACKEND", "backend"])
        assert task.tags == ["backend"]
    
    def test_empty_tags_are_filtered(self):
        """Empty tag strings are removed."""
        task = TodoTask(id=1, title="Test", tags=["valid", "", "  ", "also-valid"])
        assert task.tags == ["valid", "also-valid"]
    
    def test_all_fields_can_be_set(self):
        """Can create task with all fields populated."""
        future_date = datetime.now() + timedelta(days=7)
        task = TodoTask(
            id=1,
            title="Full task",
            description="Detailed description",
            status=Status.PENDING,
            priority=Priority.URGENT,
            tags=["work", "important"],
            due_date=future_date,
            recurrence_pattern=RecurrencePattern.WEEKLY
        )
        assert task.description == "Detailed description"
        assert task.priority == Priority.URGENT
        assert task.recurrence_pattern == RecurrencePattern.WEEKLY


class TestTodoTaskBusinessLogic:
    """Tests for TodoTask business logic methods - T018."""
    
    def test_mark_complete_changes_status(self):
        """mark_complete() sets status to COMPLETED."""
        task = TodoTask(id=1, title="Test")
        assert task.status == Status.PENDING
        task.mark_complete()
        assert task.status == Status.COMPLETED
    
    def test_mark_complete_sets_completed_at(self):
        """mark_complete() sets completed_at timestamp."""
        task = TodoTask(id=1, title="Test")
        assert task.completed_at is None
        task.mark_complete()
        assert task.completed_at is not None
        assert isinstance(task.completed_at, datetime)
    
    def test_mark_complete_updates_updated_at(self):
        """mark_complete() updates updated_at timestamp."""
        task = TodoTask(id=1, title="Test")
        original_updated = task.updated_at
        task.mark_complete()
        assert task.updated_at >= original_updated
    
    def test_is_overdue_returns_true_for_past_due_pending(self):
        """is_overdue() returns True for past due pending tasks."""
        past_date = datetime.now() - timedelta(days=1)
        # Create task without validation to test overdue logic
        task = TodoTask(id=1, title="Test")
        task.due_date = past_date  # Direct assignment bypasses validation
        task.status = Status.PENDING
        assert task.is_overdue() is True
    
    def test_is_overdue_returns_false_for_completed(self):
        """is_overdue() returns False for completed tasks even if past due."""
        past_date = datetime.now() - timedelta(days=1)
        task = TodoTask(id=1, title="Test")
        task.due_date = past_date
        task.status = Status.COMPLETED
        assert task.is_overdue() is False
    
    def test_is_overdue_returns_false_for_no_due_date(self):
        """is_overdue() returns False for tasks without due date."""
        task = TodoTask(id=1, title="Test")
        assert task.is_overdue() is False
    
    def test_has_recurrence_returns_true_for_recurring(self):
        """has_recurrence() returns True for recurring tasks."""
        task = TodoTask(id=1, title="Test", recurrence_pattern=RecurrencePattern.DAILY)
        assert task.has_recurrence() is True
    
    def test_has_recurrence_returns_false_for_none(self):
        """has_recurrence() returns False for non-recurring tasks."""
        task = TodoTask(id=1, title="Test", recurrence_pattern=RecurrencePattern.NONE)
        assert task.has_recurrence() is False


class TestTodoTaskSerialization:
    """Tests for TodoTask serialization - T020."""
    
    def test_to_dict_returns_dictionary(self):
        """to_dict() returns a dictionary."""
        task = TodoTask(id=1, title="Test")
        result = task.to_dict()
        assert isinstance(result, dict)
    
    def test_to_dict_includes_all_fields(self):
        """to_dict() includes all model fields."""
        task = TodoTask(id=1, title="Test", tags=["work"])
        result = task.to_dict()
        assert "id" in result
        assert "title" in result
        assert "description" in result
        assert "status" in result
        assert "priority" in result
        assert "tags" in result
        assert "due_date" in result
        assert "recurrence_pattern" in result
        assert "created_at" in result
        assert "updated_at" in result
        assert "completed_at" in result
    
    def test_to_dict_serializes_enums_as_strings(self):
        """to_dict() converts enums to string values."""
        task = TodoTask(id=1, title="Test", priority=Priority.URGENT)
        result = task.to_dict()
        assert result["priority"] == "urgent"
        assert result["status"] == "pending"
    
    def test_to_dict_serializes_datetime_as_iso(self):
        """to_dict() converts datetime to ISO string."""
        task = TodoTask(id=1, title="Test")
        result = task.to_dict()
        assert isinstance(result["created_at"], str)
        # Should be parseable as ISO format
        datetime.fromisoformat(result["created_at"])
    
    def test_from_dict_creates_task(self):
        """from_dict() creates TodoTask from dictionary."""
        task = TodoTask(id=1, title="Test", tags=["work"])
        dict_data = task.to_dict()
        restored = TodoTask.from_dict(dict_data)
        assert restored.id == task.id
        assert restored.title == task.title
    
    def test_roundtrip_serialization(self):
        """Task survives to_dict → from_dict roundtrip."""
        future_date = datetime.now() + timedelta(days=7)
        original = TodoTask(
            id=42,
            title="Roundtrip test",
            description="Full description",
            priority=Priority.HIGH,
            tags=["roundtrip", "test"],
            due_date=future_date,
            recurrence_pattern=RecurrencePattern.WEEKLY
        )
        
        dict_data = original.to_dict()
        restored = TodoTask.from_dict(dict_data)
        
        assert restored.id == original.id
        assert restored.title == original.title
        assert restored.description == original.description
        assert restored.priority == original.priority
        assert restored.tags == original.tags
        assert restored.recurrence_pattern == original.recurrence_pattern


class TestTodoTaskDisplay:
    """Tests for TodoTask display formatting methods."""
    
    def test_format_priority_badge(self):
        """format_priority_badge() returns Rich markup."""
        task = TodoTask(id=1, title="Test", priority=Priority.URGENT)
        badge = task.format_priority_badge()
        assert "red" in badge
        assert "URGENT" in badge
        assert "🔴" in badge
    
    def test_format_status_badge(self):
        """format_status_badge() returns Rich markup."""
        task = TodoTask(id=1, title="Test")
        badge = task.format_status_badge()
        assert "Pending" in badge or "pending" in badge.lower()
    
    def test_format_tags_display_with_tags(self):
        """format_tags_display() shows tags with hashtags."""
        task = TodoTask(id=1, title="Test", tags=["work", "important"])
        display = task.format_tags_display()
        assert "#work" in display
        assert "#important" in display
    
    def test_format_tags_display_without_tags(self):
        """format_tags_display() shows 'No tags' when empty."""
        task = TodoTask(id=1, title="Test", tags=[])
        display = task.format_tags_display()
        assert "No tags" in display
