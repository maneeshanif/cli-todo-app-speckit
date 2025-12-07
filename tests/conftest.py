"""
Pytest configuration and shared fixtures for Retro Todo tests.
"""
import pytest
import os
import tempfile
from pathlib import Path


@pytest.fixture
def temp_db_path():
    """Create a temporary database file for testing."""
    with tempfile.NamedTemporaryFile(suffix='.json', delete=False) as f:
        temp_path = f.name
    yield temp_path
    # Cleanup after test
    if os.path.exists(temp_path):
        os.remove(temp_path)


@pytest.fixture
def sample_task_data():
    """Sample task data for testing."""
    return {
        'title': 'Test Task',
        'description': 'A sample task for testing',
        'priority': 'medium',
        'tags': ['test', 'sample'],
    }


@pytest.fixture(autouse=True)
def reset_database():
    """Reset database state between tests."""
    # Import here to avoid circular imports
    from retro_todo.database import db as database_module
    
    # Store original path
    original_path = getattr(database_module, '_db_path', None)
    
    yield
    
    # Reset database module state after each test
    if hasattr(database_module, '_db'):
        database_module._db = None
    if hasattr(database_module, '_tasks_table'):
        database_module._tasks_table = None
