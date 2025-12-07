"""
Integration tests for database operations.

Tests T022, T026: RED phase tests for database initialization and CRUD.
"""
import pytest
import os
import tempfile
from retro_todo.database.db import (
    get_database, 
    get_tasks_table, 
    init_database,
    insert_task,
    get_task,
    get_all_tasks,
    update_task,
    delete_task,
    close_database
)
from retro_todo.models.todo import TodoTask
from retro_todo.models.enums import Priority, Status


class TestDatabaseInitialization:
    """Tests for database initialization - T022."""
    
    def test_database_can_be_initialized(self, temp_db_path):
        """Database initializes successfully."""
        db = init_database(temp_db_path)
        assert db is not None
        close_database()
    
    def test_database_creates_file(self, temp_db_path):
        """Database creates JSON file on disk."""
        init_database(temp_db_path)
        assert os.path.exists(temp_db_path)
        close_database()
    
    def test_get_tasks_table_returns_table(self, temp_db_path):
        """get_tasks_table returns a table instance."""
        init_database(temp_db_path)
        table = get_tasks_table()
        assert table is not None
        close_database()


class TestDatabaseCRUD:
    """Tests for database CRUD operations - T026."""
    
    def test_insert_task(self, temp_db_path):
        """Can insert a task into database."""
        init_database(temp_db_path)
        task = TodoTask(id=1, title="Test task", priority=Priority.HIGH)
        doc_id = insert_task(task)
        assert doc_id is not None
        close_database()
    
    def test_get_task_by_id(self, temp_db_path):
        """Can retrieve task by ID."""
        init_database(temp_db_path)
        task = TodoTask(id=1, title="Test task")
        insert_task(task)
        
        retrieved = get_task(1)
        assert retrieved is not None
        assert retrieved.id == 1
        assert retrieved.title == "Test task"
        close_database()
    
    def test_get_nonexistent_task(self, temp_db_path):
        """Returns None for nonexistent task."""
        init_database(temp_db_path)
        retrieved = get_task(999)
        assert retrieved is None
        close_database()
    
    def test_get_all_tasks(self, temp_db_path):
        """Can retrieve all tasks."""
        init_database(temp_db_path)
        task1 = TodoTask(id=1, title="Task 1")
        task2 = TodoTask(id=2, title="Task 2")
        insert_task(task1)
        insert_task(task2)
        
        all_tasks = get_all_tasks()
        assert len(all_tasks) == 2
        close_database()
    
    def test_update_task(self, temp_db_path):
        """Can update an existing task."""
        init_database(temp_db_path)
        task = TodoTask(id=1, title="Original title")
        insert_task(task)
        
        task.title = "Updated title"
        update_task(task)
        
        retrieved = get_task(1)
        assert retrieved.title == "Updated title"
        close_database()
    
    def test_delete_task(self, temp_db_path):
        """Can delete a task."""
        init_database(temp_db_path)
        task = TodoTask(id=1, title="To be deleted")
        insert_task(task)
        
        delete_task(1)
        
        retrieved = get_task(1)
        assert retrieved is None
        close_database()
    
    def test_data_persists_after_close(self, temp_db_path):
        """Data persists after closing and reopening database."""
        init_database(temp_db_path)
        task = TodoTask(id=1, title="Persistent task")
        insert_task(task)
        close_database()
        
        # Reopen
        init_database(temp_db_path)
        retrieved = get_task(1)
        assert retrieved is not None
        assert retrieved.title == "Persistent task"
        close_database()
