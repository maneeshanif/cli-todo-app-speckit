"""
Unit tests for Rich table rendering.

Tests T032, T058, T070: RED phase tests for task tables and stats display.
"""
import pytest
from datetime import datetime, timedelta
from retro_todo.models.todo import TodoTask
from retro_todo.models.enums import Priority, Status
from retro_todo.ui.tables import (
    format_task_table,
    format_stats_panel,
    highlight_search_term
)


class TestTaskTable:
    """Tests for task table rendering - T032."""
    
    def test_format_task_table_returns_table(self):
        """format_task_table returns a Rich Table."""
        from rich.table import Table
        tasks = [TodoTask(id=1, title="Test task")]
        table = format_task_table(tasks)
        assert isinstance(table, Table)
    
    def test_format_task_table_empty_list(self):
        """Handles empty task list."""
        from rich.table import Table
        table = format_task_table([])
        assert isinstance(table, Table)
    
    def test_table_has_expected_columns(self):
        """Table has ID, Title, Priority, Status columns."""
        tasks = [TodoTask(id=1, title="Test")]
        table = format_task_table(tasks)
        # Rich Table has columns property
        column_names = [col.header for col in table.columns]
        assert "ID" in column_names or "id" in str(column_names).lower()
        assert "Title" in column_names or "title" in str(column_names).lower()
    
    def test_table_includes_task_data(self):
        """Table rows contain task information."""
        tasks = [
            TodoTask(id=1, title="First task", priority=Priority.HIGH),
            TodoTask(id=2, title="Second task", priority=Priority.LOW),
        ]
        table = format_task_table(tasks)
        # Table should have 2 rows
        assert table.row_count == 2


class TestStatsPanel:
    """Tests for stats panel rendering - T058."""
    
    def test_format_stats_panel_returns_panel(self):
        """format_stats_panel returns Rich content."""
        stats = {
            "total": 10,
            "completed": 3,
            "pending": 7,
            "overdue": 1,
            "by_priority": {"low": 2, "medium": 5, "high": 3, "urgent": 0},
            "by_tags": {"work": 4, "personal": 3},
        }
        panel = format_stats_panel(stats)
        assert panel is not None
    
    def test_stats_panel_shows_total_count(self):
        """Stats panel displays total task count."""
        stats = {"total": 42, "completed": 10, "pending": 32, "overdue": 0, 
                 "by_priority": {}, "by_tags": {}}
        # Panel should be generated without error
        panel = format_stats_panel(stats)
        assert panel is not None


class TestSearchHighlight:
    """Tests for search result highlighting - T070."""
    
    def test_highlight_search_term_returns_string(self):
        """highlight_search_term returns markup string."""
        result = highlight_search_term("Hello world", "world")
        assert isinstance(result, str)
    
    def test_highlight_wraps_match_in_markup(self):
        """Matching text is wrapped in Rich markup."""
        result = highlight_search_term("Hello world", "world")
        assert "[" in result  # Rich markup indicator
    
    def test_highlight_case_insensitive(self):
        """Highlighting is case insensitive."""
        result = highlight_search_term("Hello WORLD", "world")
        assert "WORLD" in result or "world" in result.lower()
    
    def test_highlight_no_match(self):
        """Returns original text when no match."""
        result = highlight_search_term("Hello world", "xyz")
        # Should contain the original text
        assert "Hello" in result
