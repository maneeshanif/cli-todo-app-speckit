"""
End-to-end tests for CLI commands.

Tests T042, T045, T047, T049: RED phase tests for CLI command execution.
"""
import pytest
from typer.testing import CliRunner
from retro_todo.main import app


runner = CliRunner()


class TestSplashCommand:
    """Tests for splash command - T042."""
    
    def test_splash_command_exits_ok(self):
        """Splash command runs without error."""
        result = runner.invoke(app, ["splash"])
        assert result.exit_code == 0
    
    def test_splash_displays_content(self):
        """Splash command displays content."""
        result = runner.invoke(app, ["splash"])
        # Should contain some output
        assert len(result.output) > 0
    
    def test_splash_includes_developer_credit(self):
        """Splash includes maneeshanif credit."""
        result = runner.invoke(app, ["splash"])
        assert "maneeshanif" in result.output


class TestAddCommand:
    """Tests for add command - T045."""
    
    def test_add_command_exists(self):
        """Add command is registered."""
        result = runner.invoke(app, ["add", "--help"])
        assert result.exit_code == 0
    
    def test_add_with_title_option(self):
        """Can add task with --title option."""
        result = runner.invoke(app, [
            "add", "--title", "Test task", "--no-interactive"
        ])
        assert result.exit_code == 0
    
    def test_add_with_priority_option(self):
        """Can add task with --priority option."""
        result = runner.invoke(app, [
            "add", "--title", "Priority task", 
            "--priority", "high", "--no-interactive"
        ])
        assert result.exit_code == 0


class TestListCommand:
    """Tests for list command - T047."""
    
    def test_list_command_exists(self):
        """List command is registered."""
        result = runner.invoke(app, ["list", "--help"])
        assert result.exit_code == 0
    
    def test_list_shows_tasks(self):
        """List command displays task table."""
        result = runner.invoke(app, ["list"])
        assert result.exit_code == 0


class TestCompleteCommand:
    """Tests for complete command - T049."""
    
    def test_complete_command_exists(self):
        """Complete command is registered."""
        result = runner.invoke(app, ["complete", "--help"])
        assert result.exit_code == 0


class TestStatsCommand:
    """Tests for stats command - T062."""
    
    def test_stats_command_exists(self):
        """Stats command is registered."""
        result = runner.invoke(app, ["stats"])
        assert result.exit_code == 0


class TestSearchCommand:
    """Tests for search command - T074."""
    
    def test_search_command_exists(self):
        """Search command is registered."""
        result = runner.invoke(app, ["search", "--help"])
        assert result.exit_code == 0


class TestUpdateCommand:
    """Tests for update command - T090."""
    
    def test_update_command_exists(self):
        """Update command is registered."""
        result = runner.invoke(app, ["update", "--help"])
        assert result.exit_code == 0


class TestDeleteCommand:
    """Tests for delete command - T092."""
    
    def test_delete_command_exists(self):
        """Delete command is registered."""
        result = runner.invoke(app, ["delete", "--help"])
        assert result.exit_code == 0
