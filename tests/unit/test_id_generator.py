"""
Unit tests for ID generator.

Tests T024: RED phase tests for atomic ID generation.
"""
import pytest
from retro_todo.database.id_generator import generate_task_id


class TestIdGenerator:
    """Tests for atomic ID generation - T024."""
    
    def test_generate_returns_integer(self):
        """generate_task_id returns an integer."""
        task_id = generate_task_id([])
        assert isinstance(task_id, int)
    
    def test_generate_returns_1_for_empty_list(self):
        """First task gets ID 1."""
        task_id = generate_task_id([])
        assert task_id == 1
    
    def test_generate_returns_next_id(self):
        """New ID is max existing + 1."""
        existing = [{'id': 1}, {'id': 2}, {'id': 3}]
        task_id = generate_task_id(existing)
        assert task_id == 4
    
    def test_generate_handles_gaps(self):
        """Handles gaps in ID sequence."""
        existing = [{'id': 1}, {'id': 5}, {'id': 10}]
        task_id = generate_task_id(existing)
        assert task_id == 11
    
    def test_generate_handles_unordered_ids(self):
        """Handles IDs not in order."""
        existing = [{'id': 5}, {'id': 1}, {'id': 3}]
        task_id = generate_task_id(existing)
        assert task_id == 6
