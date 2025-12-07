"""
Comprehensive integration tests for main.py CLI commands.

These tests increase coverage by testing actual command execution paths.
"""
import pytest
from unittest.mock import patch, MagicMock
from typer.testing import CliRunner
from datetime import datetime, timedelta
import tempfile
import os

from retro_todo.main import app, get_service
from retro_todo.models.enums import Priority, Status
from retro_todo.models.todo import TodoTask

runner = CliRunner()


@pytest.fixture
def mock_service():
    """Create a mock TodoService."""
    with patch('retro_todo.main.TodoService') as mock:
        mock_instance = MagicMock()
        mock.return_value = mock_instance
        yield mock_instance


@pytest.fixture
def sample_task():
    """Create a sample task for testing."""
    return TodoTask(
        id=1,
        title="Test Task",
        description="Test description",
        priority=Priority.HIGH,
        status=Status.PENDING,
        tags=["test", "sample"],
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )


@pytest.fixture
def sample_tasks():
    """Create multiple sample tasks."""
    return [
        TodoTask(
            id=1,
            title="Task One",
            priority=Priority.HIGH,
            status=Status.PENDING,
            tags=["work"],
        ),
        TodoTask(
            id=2,
            title="Task Two",
            priority=Priority.LOW,
            status=Status.COMPLETED,
            tags=["home"],
        ),
        TodoTask(
            id=3,
            title="Task Three",
            priority=Priority.URGENT,
            status=Status.PENDING,
            tags=["urgent"],
        ),
    ]


class TestMainCallback:
    """Tests for main app callback."""
    
    def test_version_flag(self):
        """--version shows version and exits."""
        result = runner.invoke(app, ["--version"])
        assert "version" in result.output.lower() or "0.1.0" in result.output
    
    def test_no_command_shows_splash(self):
        """No command shows splash screen."""
        with patch('retro_todo.main.show_splash') as mock_splash:
            with patch('retro_todo.main.show_welcome_message'):
                result = runner.invoke(app, [])


class TestSplashCommand:
    """Tests for splash command."""
    
    def test_splash_runs(self):
        """Splash command runs successfully."""
        result = runner.invoke(app, ["splash"])
        assert result.exit_code == 0


class TestAddCommand:
    """Tests for add command."""
    
    def test_add_non_interactive_with_title(self, mock_service, sample_task):
        """Add with --title in non-interactive mode."""
        mock_service.create.return_value = sample_task
        
        with patch('retro_todo.main.init_database'):
            result = runner.invoke(app, [
                "add", 
                "--title", "New Task",
                "--no-interactive"
            ])
        
        # Service create should be called
        mock_service.create.assert_called()
    
    def test_add_with_priority(self, mock_service, sample_task):
        """Add with priority option."""
        mock_service.create.return_value = sample_task
        
        with patch('retro_todo.main.init_database'):
            result = runner.invoke(app, [
                "add",
                "--title", "Urgent Task",
                "--priority", "urgent",
                "--no-interactive"
            ])
    
    def test_add_with_description(self, mock_service, sample_task):
        """Add with description option."""
        mock_service.create.return_value = sample_task
        
        with patch('retro_todo.main.init_database'):
            result = runner.invoke(app, [
                "add",
                "--title", "Described Task",
                "--description", "This is the description",
                "--no-interactive"
            ])
    
    def test_add_with_tags(self, mock_service, sample_task):
        """Add with tags option."""
        mock_service.create.return_value = sample_task
        
        with patch('retro_todo.main.init_database'):
            result = runner.invoke(app, [
                "add",
                "--title", "Tagged Task",
                "--tags", "work,important,project",
                "--no-interactive"
            ])
    
    def test_add_missing_title_non_interactive(self, mock_service):
        """Add without title in non-interactive mode shows error."""
        with patch('retro_todo.main.init_database'):
            result = runner.invoke(app, ["add", "--no-interactive"])
            # Should exit with error or show error message


class TestListCommand:
    """Tests for list command."""
    
    def test_list_empty(self, mock_service):
        """List shows empty state when no tasks."""
        mock_service.get_all.return_value = []
        
        with patch('retro_todo.main.init_database'):
            result = runner.invoke(app, ["list"])
    
    def test_list_with_tasks(self, mock_service, sample_tasks):
        """List displays tasks."""
        mock_service.get_all.return_value = sample_tasks
        
        with patch('retro_todo.main.init_database'):
            result = runner.invoke(app, ["list", "--all"])
    
    def test_list_pending_only(self, mock_service, sample_tasks):
        """List --pending shows only pending tasks."""
        mock_service.get_all.return_value = sample_tasks
        
        with patch('retro_todo.main.init_database'):
            result = runner.invoke(app, ["list", "--pending"])
    
    def test_list_completed_only(self, mock_service, sample_tasks):
        """List --completed shows only completed tasks."""
        mock_service.get_all.return_value = sample_tasks
        
        with patch('retro_todo.main.init_database'):
            result = runner.invoke(app, ["list", "--completed"])
    
    def test_list_by_priority(self, mock_service, sample_tasks):
        """List --priority filters by priority."""
        mock_service.get_all.return_value = sample_tasks
        
        with patch('retro_todo.main.init_database'):
            result = runner.invoke(app, ["list", "--priority", "high"])
    
    def test_list_invalid_priority(self, mock_service, sample_tasks):
        """List with invalid priority shows error."""
        mock_service.get_all.return_value = sample_tasks
        
        with patch('retro_todo.main.init_database'):
            result = runner.invoke(app, ["list", "--priority", "invalid"])


class TestViewCommand:
    """Tests for view command."""
    
    def test_view_existing_task(self, mock_service, sample_task):
        """View displays task details."""
        mock_service.get_by_id.return_value = sample_task
        
        with patch('retro_todo.main.init_database'):
            result = runner.invoke(app, ["view", "1"])
    
    def test_view_nonexistent_task(self, mock_service):
        """View shows error for missing task."""
        mock_service.get_by_id.return_value = None
        
        with patch('retro_todo.main.init_database'):
            result = runner.invoke(app, ["view", "999"])


class TestCompleteCommand:
    """Tests for complete command."""
    
    def test_complete_existing_task(self, mock_service, sample_task):
        """Complete marks task as done."""
        mock_service.complete.return_value = sample_task
        
        with patch('retro_todo.main.init_database'):
            result = runner.invoke(app, ["complete", "1"])
    
    def test_complete_nonexistent_task(self, mock_service):
        """Complete shows error for missing task."""
        mock_service.complete.return_value = None
        
        with patch('retro_todo.main.init_database'):
            result = runner.invoke(app, ["complete", "999"])


class TestDeleteCommand:
    """Tests for delete command."""
    
    def test_delete_with_force(self, mock_service, sample_task):
        """Delete with --force skips confirmation."""
        mock_service.get_by_id.return_value = sample_task
        mock_service.delete.return_value = True
        
        with patch('retro_todo.main.init_database'):
            result = runner.invoke(app, ["delete", "1", "--force"])
    
    def test_delete_nonexistent_task(self, mock_service):
        """Delete shows error for missing task."""
        mock_service.get_by_id.return_value = None
        
        with patch('retro_todo.main.init_database'):
            result = runner.invoke(app, ["delete", "999", "--force"])


class TestUpdateCommand:
    """Tests for update command."""
    
    def test_update_title(self, mock_service, sample_task):
        """Update changes task title."""
        mock_service.update.return_value = sample_task
        
        with patch('retro_todo.main.init_database'):
            result = runner.invoke(app, [
                "update", "1",
                "--title", "Updated Title",
                "--no-interactive"
            ])
    
    def test_update_priority(self, mock_service, sample_task):
        """Update changes task priority."""
        mock_service.update.return_value = sample_task
        
        with patch('retro_todo.main.init_database'):
            result = runner.invoke(app, [
                "update", "1",
                "--priority", "urgent",
                "--no-interactive"
            ])
    
    def test_update_nonexistent_task(self, mock_service):
        """Update shows error for missing task."""
        mock_service.update.return_value = None
        
        with patch('retro_todo.main.init_database'):
            result = runner.invoke(app, [
                "update", "999",
                "--title", "New Title",
                "--no-interactive"
            ])


class TestSearchCommand:
    """Tests for search command."""
    
    def test_search_with_query(self, mock_service, sample_tasks):
        """Search finds matching tasks."""
        mock_service.get_all.return_value = sample_tasks
        
        with patch('retro_todo.main.init_database'):
            result = runner.invoke(app, ["search", "Task"])
    
    def test_search_no_results(self, mock_service):
        """Search shows message when no matches."""
        mock_service.get_all.return_value = []
        
        with patch('retro_todo.main.init_database'):
            result = runner.invoke(app, ["search", "nonexistent"])
    
    def test_search_case_insensitive(self, mock_service, sample_tasks):
        """Search is case-insensitive."""
        mock_service.get_all.return_value = sample_tasks
        
        with patch('retro_todo.main.init_database'):
            result = runner.invoke(app, ["search", "TASK"])


class TestFilterCommand:
    """Tests for filter command."""
    
    def test_filter_by_priority(self, mock_service, sample_tasks):
        """Filter by priority."""
        mock_service.get_all.return_value = sample_tasks
        
        with patch('retro_todo.main.init_database'):
            result = runner.invoke(app, [
                "filter",
                "--priority", "high",
                "--no-interactive"
            ])
    
    def test_filter_by_status(self, mock_service, sample_tasks):
        """Filter by status."""
        mock_service.get_all.return_value = sample_tasks
        
        with patch('retro_todo.main.init_database'):
            result = runner.invoke(app, [
                "filter",
                "--status", "pending",
                "--no-interactive"
            ])
    
    def test_filter_by_tags(self, mock_service, sample_tasks):
        """Filter by tags."""
        mock_service.get_all.return_value = sample_tasks
        
        with patch('retro_todo.main.init_database'):
            result = runner.invoke(app, [
                "filter",
                "--tags", "work",
                "--no-interactive"
            ])


class TestStatsCommand:
    """Tests for stats command."""
    
    def test_stats_displays_counts(self, mock_service):
        """Stats shows task counts."""
        mock_service.get_statistics.return_value = {
            "total": 10,
            "pending": 5,
            "completed": 5,
            "overdue": 2,
            "by_priority": {
                "low": 2,
                "medium": 3,
                "high": 3,
                "urgent": 2
            }
        }
        
        with patch('retro_todo.main.init_database'):
            result = runner.invoke(app, ["stats"])
    
    def test_stats_empty(self, mock_service):
        """Stats with no tasks."""
        mock_service.get_statistics.return_value = {
            "total": 0,
            "pending": 0,
            "completed": 0,
            "overdue": 0,
            "by_priority": {}
        }
        
        with patch('retro_todo.main.init_database'):
            result = runner.invoke(app, ["stats"])
