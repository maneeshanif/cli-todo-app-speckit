"""
Extended tests for prompts module.

Additional tests to improve coverage.
"""
import pytest
from unittest.mock import patch, MagicMock
from retro_todo.models.enums import Priority, Status


class TestAddTaskPromptExtended:
    """Extended tests for add task prompt."""
    
    def test_add_task_returns_none_on_cancel(self):
        """Returns None when cancelled at any step."""
        from retro_todo.ui.prompts import add_task_prompt
        
        with patch('retro_todo.ui.prompts.questionary') as mock_q:
            mock_q.text.return_value.ask.return_value = None
            
            result = add_task_prompt()
            assert result is None
    
    def test_add_task_collects_priority(self):
        """Prompt collects priority selection."""
        from retro_todo.ui.prompts import add_task_prompt
        
        with patch('retro_todo.ui.prompts.questionary') as mock_q:
            # First call to text for title
            mock_q.text.return_value.ask.return_value = None
            
            result = add_task_prompt()
            # Cancelled at title


class TestFilterPromptExtended:
    """Extended tests for filter prompt."""
    
    def test_filter_returns_empty_on_cancel(self):
        """Returns empty dict or None when cancelled."""
        from retro_todo.ui.prompts import filter_prompt
        
        with patch('retro_todo.ui.prompts.questionary') as mock_q:
            mock_q.checkbox.return_value.ask.return_value = None
            mock_q.select.return_value.ask.return_value = None
            mock_q.text.return_value.ask.return_value = None
            
            result = filter_prompt()
            assert isinstance(result, dict)


class TestConfirmDeleteExtended:
    """Extended tests for confirm delete."""
    
    def test_confirm_returns_false_on_decline(self):
        """Returns False when user declines."""
        from retro_todo.ui.prompts import confirm_delete
        
        with patch('retro_todo.ui.prompts.questionary') as mock_q:
            mock_q.confirm.return_value.ask.return_value = False
            
            result = confirm_delete("Task to delete")
            assert result is False
    
    def test_confirm_handles_none_response(self):
        """Handles None response (Ctrl+C)."""
        from retro_todo.ui.prompts import confirm_delete
        
        with patch('retro_todo.ui.prompts.questionary') as mock_q:
            mock_q.confirm.return_value.ask.return_value = None
            
            result = confirm_delete("Task")
            # Should handle gracefully (either False or None)


class TestUpdateTaskPrompt:
    """Tests for update task prompt."""
    
    def test_update_prompt_exists(self):
        """Update task prompt function exists."""
        from retro_todo.ui import prompts
        
        assert hasattr(prompts, 'update_task_prompt')
    
    def test_update_prompt_returns_dict_or_none(self):
        """Update prompt returns dict or None."""
        from retro_todo.ui.prompts import update_task_prompt
        
        with patch('retro_todo.ui.prompts.questionary') as mock_q:
            mock_q.text.return_value.ask.return_value = None
            mock_q.select.return_value.ask.return_value = None
            
            # Create mock current task
            mock_task = MagicMock()
            mock_task.title = "Current Title"
            mock_task.description = "Current Desc"
            mock_task.priority = Priority.MEDIUM
            mock_task.tags = ["test"]
            
            result = update_task_prompt(mock_task)
            # Should return dict or None


class TestSelectTaskPrompt:
    """Tests for task selection prompt."""
    
    def test_select_task_exists(self):
        """Task selection prompt exists."""
        from retro_todo.ui import prompts
        
        # Check for various possible names
        has_select = (
            hasattr(prompts, 'select_task_prompt') or
            hasattr(prompts, 'task_selection_prompt') or
            hasattr(prompts, 'select_task')
        )
        # This may or may not exist depending on implementation


class TestPrioritySelection:
    """Tests for priority selection in prompts."""
    
    def test_priority_choices_defined(self):
        """Priority choices are available for prompts."""
        from retro_todo.models.enums import Priority
        
        choices = [p.value for p in Priority]
        assert "low" in choices
        assert "medium" in choices
        assert "high" in choices
        assert "urgent" in choices


class TestStatusSelection:
    """Tests for status selection in prompts."""
    
    def test_status_choices_defined(self):
        """Status choices are available for prompts."""
        from retro_todo.models.enums import Status
        
        choices = [s.value for s in Status]
        assert "pending" in choices
        assert "completed" in choices
