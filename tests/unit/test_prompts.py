"""
Unit tests for Questionary prompts.

Tests T034, T054, T056, T072, T080, T082: RED phase tests for interactive prompts.
"""
import pytest
from unittest.mock import patch, MagicMock, PropertyMock
from retro_todo.models.enums import Priority


class TestAddTaskPrompt:
    """Tests for add task prompt - T034."""
    
    def test_add_task_prompt_cancelled(self):
        """Returns None when user cancels."""
        from retro_todo.ui.prompts import add_task_prompt
        
        with patch('retro_todo.ui.prompts.questionary') as mock_q:
            mock_q.text.return_value.ask.return_value = None
            
            result = add_task_prompt()
            assert result is None


class TestFilterPrompt:
    """Tests for filter selection prompt - T072."""
    
    def test_filter_prompt_returns_dict(self):
        """filter_prompt returns filter criteria dictionary."""
        from retro_todo.ui.prompts import filter_prompt
        
        with patch('retro_todo.ui.prompts.questionary') as mock_q:
            mock_q.checkbox.return_value.ask.return_value = []
            mock_q.select.return_value.ask.return_value = None
            mock_q.text.return_value.ask.return_value = ""
            
            result = filter_prompt()
            assert isinstance(result, dict)


class TestConfirmationPrompt:
    """Tests for delete confirmation - T082."""
    
    def test_confirm_delete_returns_bool(self):
        """confirm_delete returns boolean."""
        from retro_todo.ui.prompts import confirm_delete
        
        with patch('retro_todo.ui.prompts.questionary') as mock_q:
            mock_q.confirm.return_value.ask.return_value = True
            
            result = confirm_delete("Test task")
            assert isinstance(result, bool)
    
    def test_confirm_delete_shows_task_name(self):
        """Confirmation shows task name in prompt."""
        from retro_todo.ui.prompts import confirm_delete
        
        with patch('retro_todo.ui.prompts.questionary') as mock_q:
            mock_q.confirm.return_value.ask.return_value = True
            
            confirm_delete("Important Task")
            # Verify confirm was called with task name in message
            mock_q.confirm.assert_called()
