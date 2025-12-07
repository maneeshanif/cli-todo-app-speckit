"""
Unit tests for enumeration types.

Tests T010, T012, T014: RED phase tests for Priority, Status, RecurrencePattern enums.
"""
import pytest
from retro_todo.models.enums import Priority, Status, RecurrencePattern


class TestPriority:
    """Tests for Priority enum - T010."""
    
    def test_priority_values_exist(self):
        """Priority enum has LOW, MEDIUM, HIGH, URGENT values."""
        assert Priority.LOW.value == "low"
        assert Priority.MEDIUM.value == "medium"
        assert Priority.HIGH.value == "high"
        assert Priority.URGENT.value == "urgent"
    
    def test_priority_color_property(self):
        """Each priority has a color for Rich terminal display."""
        assert Priority.LOW.color == "green"
        assert Priority.MEDIUM.color == "yellow"
        assert Priority.HIGH.color == "orange1"
        assert Priority.URGENT.color == "red"
    
    def test_priority_icon_property(self):
        """Each priority has an emoji icon."""
        assert Priority.LOW.icon == "🟢"
        assert Priority.MEDIUM.icon == "🟡"
        assert Priority.HIGH.icon == "🟠"
        assert Priority.URGENT.icon == "🔴"
    
    def test_priority_is_string_enum(self):
        """Priority inherits from str for JSON serialization."""
        assert isinstance(Priority.LOW, str)
        assert Priority.LOW.value == "low"


class TestStatus:
    """Tests for Status enum - T012."""
    
    def test_status_values_exist(self):
        """Status enum has PENDING and COMPLETED values."""
        assert Status.PENDING.value == "pending"
        assert Status.COMPLETED.value == "completed"
    
    def test_status_icon_property(self):
        """Each status has an emoji icon."""
        assert Status.PENDING.icon == "⏳"
        assert Status.COMPLETED.icon == "✅"
    
    def test_status_display_style_property(self):
        """Completed status has strikethrough style."""
        assert Status.PENDING.display_style == ""
        assert Status.COMPLETED.display_style == "strike dim"
    
    def test_status_is_string_enum(self):
        """Status inherits from str for JSON serialization."""
        assert isinstance(Status.PENDING, str)


class TestRecurrencePattern:
    """Tests for RecurrencePattern enum - T014."""
    
    def test_recurrence_values_exist(self):
        """RecurrencePattern enum has all values."""
        assert RecurrencePattern.NONE.value == "none"
        assert RecurrencePattern.DAILY.value == "daily"
        assert RecurrencePattern.WEEKLY.value == "weekly"
        assert RecurrencePattern.MONTHLY.value == "monthly"
    
    def test_recurrence_icon_property(self):
        """Recurring patterns have recurrence icon."""
        assert RecurrencePattern.NONE.icon == ""
        assert RecurrencePattern.DAILY.icon == "🔁"
        assert RecurrencePattern.WEEKLY.icon == "🔁"
        assert RecurrencePattern.MONTHLY.icon == "🔁"
    
    def test_recurrence_display_label_property(self):
        """Recurring patterns have display label."""
        assert RecurrencePattern.NONE.display_label == ""
        assert RecurrencePattern.DAILY.display_label == "🔁 Daily"
        assert RecurrencePattern.WEEKLY.display_label == "🔁 Weekly"
        assert RecurrencePattern.MONTHLY.display_label == "🔁 Monthly"
    
    def test_recurrence_is_string_enum(self):
        """RecurrencePattern inherits from str for JSON serialization."""
        assert isinstance(RecurrencePattern.NONE, str)
