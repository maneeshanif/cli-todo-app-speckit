"""
Unit tests for UI animations.

Tests for completion and loading animations.
"""
import pytest
from unittest.mock import patch, MagicMock
from rich.console import Console


class TestCompletionCelebration:
    """Tests for completion celebration animation."""
    
    def test_show_completion_celebration_runs_without_error(self):
        """Celebration runs without errors."""
        from retro_todo.ui.animations import show_completion_celebration
        
        with patch('retro_todo.ui.animations.console') as mock_console:
            # Should not raise
            show_completion_celebration("Test Task")
    
    def test_completion_celebration_accepts_task_name(self):
        """Celebration accepts task name parameter."""
        from retro_todo.ui.animations import show_completion_celebration
        
        with patch('retro_todo.ui.animations.console') as mock_console:
            show_completion_celebration("My Important Task")
            # Should complete without error
    
    def test_completion_celebration_prints_output(self):
        """Celebration prints to console."""
        from retro_todo.ui.animations import show_completion_celebration
        
        with patch('retro_todo.ui.animations.console') as mock_console:
            show_completion_celebration("Test")
            # Console.print should be called
            assert mock_console.print.called


class TestLoadingSpinner:
    """Tests for loading spinner."""
    
    def test_show_loading_spinner_returns_progress(self):
        """Loading spinner returns Progress object."""
        from retro_todo.ui.animations import show_loading_spinner
        from rich.progress import Progress
        
        result = show_loading_spinner("Loading...")
        assert isinstance(result, Progress)
    
    def test_loading_spinner_accepts_message(self):
        """Spinner accepts message parameter."""
        from retro_todo.ui.animations import show_loading_spinner
        
        result = show_loading_spinner("Processing tasks...")
        assert result is not None
    
    def test_loading_spinner_default_message(self):
        """Spinner has default message."""
        from retro_todo.ui.animations import show_loading_spinner
        
        result = show_loading_spinner()
        assert result is not None


class TestSuccessMessage:
    """Tests for success message."""
    
    def test_show_success_message_runs(self):
        """Success message displays without error."""
        from retro_todo.ui.animations import show_success_message
        
        with patch('retro_todo.ui.animations.console') as mock_console:
            show_success_message("Task created!")
            mock_console.print.assert_called()
    
    def test_success_message_contains_text(self):
        """Success message includes provided text."""
        from retro_todo.ui.animations import show_success_message
        
        with patch('retro_todo.ui.animations.console') as mock_console:
            show_success_message("Done!")
            call_args = mock_console.print.call_args[0][0]
            assert "Done!" in call_args


class TestErrorMessage:
    """Tests for error message."""
    
    def test_show_error_message_runs(self):
        """Error message displays without error."""
        from retro_todo.ui.animations import show_error_message
        
        with patch('retro_todo.ui.animations.console') as mock_console:
            show_error_message("Something went wrong")
            mock_console.print.assert_called()
    
    def test_error_message_contains_text(self):
        """Error message includes provided text."""
        from retro_todo.ui.animations import show_error_message
        
        with patch('retro_todo.ui.animations.console') as mock_console:
            show_error_message("Failed!")
            call_args = mock_console.print.call_args[0][0]
            assert "Failed!" in call_args


class TestWarningMessage:
    """Tests for warning message."""
    
    def test_show_warning_message_runs(self):
        """Warning message displays without error."""
        from retro_todo.ui.animations import show_warning_message
        
        with patch('retro_todo.ui.animations.console') as mock_console:
            show_warning_message("Be careful")
            mock_console.print.assert_called()


class TestInfoMessage:
    """Tests for info message."""
    
    def test_show_info_message_runs(self):
        """Info message displays without error."""
        from retro_todo.ui.animations import show_info_message
        
        with patch('retro_todo.ui.animations.console') as mock_console:
            show_info_message("FYI...")
            mock_console.print.assert_called()
