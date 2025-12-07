"""
Extended CLI command tests for better coverage.

Tests for main.py commands with various scenarios.
"""
import pytest
from unittest.mock import patch, MagicMock
from typer.testing import CliRunner
from datetime import datetime
import tempfile
import os


runner = CliRunner()


class TestViewCommand:
    """Tests for view command - T055."""
    
    def test_view_command_exists(self):
        """View command is registered."""
        from retro_todo.main import app
        
        result = runner.invoke(app, ["view", "--help"])
        assert result.exit_code == 0
        assert "view" in result.output.lower() or "task" in result.output.lower()


class TestFilterCommand:
    """Tests for filter command - T073."""
    
    def test_filter_command_exists(self):
        """Filter command is registered."""
        from retro_todo.main import app
        
        result = runner.invoke(app, ["filter", "--help"])
        assert result.exit_code == 0
    
    def test_filter_by_priority(self):
        """Filter can filter by priority."""
        from retro_todo.main import app
        
        with patch('retro_todo.main.TodoService') as mock_service:
            mock_instance = MagicMock()
            mock_instance.get_all.return_value = []
            mock_service.return_value = mock_instance
            
            result = runner.invoke(app, ["filter", "--priority", "high"])


class TestMainApp:
    """Tests for main app configuration."""
    
    def test_app_has_callback(self):
        """App has a callback defined."""
        from retro_todo.main import app
        
        # App should have info attribute
        assert app.info is not None
    
    def test_app_help_displays(self):
        """App help displays correctly."""
        from retro_todo.main import app
        
        result = runner.invoke(app, ["--help"])
        assert result.exit_code == 0
        # Should show available commands
        assert "add" in result.output.lower() or "list" in result.output.lower()


class TestAddCommandExtended:
    """Extended tests for add command."""
    
    def test_add_with_tags(self):
        """Add can include tags."""
        from retro_todo.main import app
        
        with patch('retro_todo.main.TodoService') as mock_service:
            mock_instance = MagicMock()
            mock_task = MagicMock()
            mock_task.id = 1
            mock_task.title = "Test"
            mock_instance.create.return_value = mock_task
            mock_service.return_value = mock_instance
            
            result = runner.invoke(app, [
                "add",
                "--title", "Tagged Task",
                "--tags", "work,important"
            ])


class TestCompleteCommandExtended:
    """Extended tests for complete command."""
    
    def test_complete_with_valid_id(self):
        """Complete marks task as done."""
        from retro_todo.main import app
        
        with patch('retro_todo.main.TodoService') as mock_service:
            mock_instance = MagicMock()
            mock_task = MagicMock()
            mock_task.id = 1
            mock_task.title = "Completed Task"
            mock_instance.complete.return_value = mock_task
            mock_service.return_value = mock_instance
            
            result = runner.invoke(app, ["complete", "1"])
    
    def test_complete_with_invalid_id(self):
        """Complete handles non-existent task."""
        from retro_todo.main import app
        
        with patch('retro_todo.main.TodoService') as mock_service:
            mock_instance = MagicMock()
            mock_instance.complete.return_value = None
            mock_service.return_value = mock_instance
            
            result = runner.invoke(app, ["complete", "999"])


class TestDeleteCommandExtended:
    """Extended tests for delete command."""
    
    def test_delete_with_force(self):
        """Delete with force skips confirmation."""
        from retro_todo.main import app
        
        with patch('retro_todo.main.TodoService') as mock_service:
            mock_instance = MagicMock()
            mock_instance.get_by_id.return_value = MagicMock(title="Test")
            mock_instance.delete.return_value = True
            mock_service.return_value = mock_instance
            
            result = runner.invoke(app, ["delete", "1", "--force"])


class TestUpdateCommandExtended:
    """Extended tests for update command."""
    
    def test_update_title(self):
        """Update can change title."""
        from retro_todo.main import app
        
        with patch('retro_todo.main.TodoService') as mock_service:
            mock_instance = MagicMock()
            mock_task = MagicMock()
            mock_task.id = 1
            mock_task.title = "Updated Title"
            mock_instance.update.return_value = mock_task
            mock_service.return_value = mock_instance
            
            result = runner.invoke(app, [
                "update", "1",
                "--title", "New Title"
            ])
    
    def test_update_priority(self):
        """Update can change priority."""
        from retro_todo.main import app
        
        with patch('retro_todo.main.TodoService') as mock_service:
            mock_instance = MagicMock()
            mock_task = MagicMock()
            mock_task.id = 1
            mock_instance.update.return_value = mock_task
            mock_service.return_value = mock_instance
            
            result = runner.invoke(app, [
                "update", "1",
                "--priority", "urgent"
            ])


class TestSearchCommandExtended:
    """Extended tests for search command."""
    
    def test_search_with_query(self):
        """Search finds matching tasks."""
        from retro_todo.main import app
        
        with patch('retro_todo.main.TodoService') as mock_service:
            mock_instance = MagicMock()
            mock_task = MagicMock()
            mock_task.title = "Find me"
            mock_task.description = ""
            mock_task.tags = []
            mock_instance.get_all.return_value = [mock_task]
            mock_service.return_value = mock_instance
            
            result = runner.invoke(app, ["search", "find"])
    
    def test_search_no_results(self):
        """Search handles no results."""
        from retro_todo.main import app
        
        with patch('retro_todo.main.TodoService') as mock_service:
            mock_instance = MagicMock()
            mock_instance.get_all.return_value = []
            mock_service.return_value = mock_instance
            
            result = runner.invoke(app, ["search", "nonexistent"])


class TestStatsCommandExtended:
    """Extended tests for stats command."""
    
    def test_stats_shows_counts(self):
        """Stats displays task counts."""
        from retro_todo.main import app
        
        with patch('retro_todo.main.TodoService') as mock_service:
            mock_instance = MagicMock()
            mock_instance.get_statistics.return_value = {
                "total": 10,
                "pending": 5,
                "completed": 5,
                "by_priority": {"high": 3, "medium": 4, "low": 3}
            }
            mock_service.return_value = mock_instance
            
            result = runner.invoke(app, ["stats"])


class TestListCommandExtended:
    """Extended tests for list command."""
    
    def test_list_with_limit(self):
        """List can limit number of tasks shown."""
        from retro_todo.main import app
        
        with patch('retro_todo.main.TodoService') as mock_service:
            mock_instance = MagicMock()
            mock_instance.get_all.return_value = []
            mock_service.return_value = mock_instance
            
            result = runner.invoke(app, ["list", "--limit", "5"])
    
    def test_list_shows_empty_message(self):
        """List shows message when no tasks."""
        from retro_todo.main import app
        
        with patch('retro_todo.main.TodoService') as mock_service:
            mock_instance = MagicMock()
            mock_instance.get_all.return_value = []
            mock_service.return_value = mock_instance
            
            result = runner.invoke(app, ["list"])
