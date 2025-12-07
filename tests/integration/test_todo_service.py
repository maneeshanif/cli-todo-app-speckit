"""
Integration tests for TodoService.

Tests T036, T038, T040: RED phase tests for service CRUD operations.
"""
import pytest
import tempfile
import os
from retro_todo.services.todo_service import TodoService
from retro_todo.database.db import init_database, close_database
from retro_todo.models.enums import Priority, Status


class TestTodoServiceCreate:
    """Tests for TodoService.create() - T036."""
    
    @pytest.fixture(autouse=True)
    def setup_service(self, temp_db_path):
        """Initialize database before each test."""
        init_database(temp_db_path)
        self.service = TodoService()
        yield
        close_database()
    
    def test_create_task_with_title(self):
        """Can create task with just title."""
        task = self.service.create(title="Test task")
        assert task is not None
        assert task.title == "Test task"
        assert task.id == 1
    
    def test_create_task_with_priority(self):
        """Can create task with priority."""
        task = self.service.create(title="High priority", priority=Priority.HIGH)
        assert task.priority == Priority.HIGH
    
    def test_create_task_with_description(self):
        """Can create task with description."""
        task = self.service.create(
            title="With desc", 
            description="Detailed description"
        )
        assert task.description == "Detailed description"
    
    def test_create_task_with_tags(self):
        """Can create task with tags."""
        task = self.service.create(
            title="Tagged task",
            tags=["work", "important"]
        )
        assert "work" in task.tags
        assert "important" in task.tags
    
    def test_create_auto_generates_id(self):
        """IDs are auto-incremented."""
        task1 = self.service.create(title="First")
        task2 = self.service.create(title="Second")
        assert task1.id == 1
        assert task2.id == 2


class TestTodoServiceGetAll:
    """Tests for TodoService.get_all() - T038."""
    
    @pytest.fixture(autouse=True)
    def setup_service(self, temp_db_path):
        """Initialize database before each test."""
        init_database(temp_db_path)
        self.service = TodoService()
        yield
        close_database()
    
    def test_get_all_empty(self):
        """Returns empty list when no tasks."""
        tasks = self.service.get_all()
        assert tasks == []
    
    def test_get_all_returns_all_tasks(self):
        """Returns all created tasks."""
        self.service.create(title="Task 1")
        self.service.create(title="Task 2")
        self.service.create(title="Task 3")
        
        tasks = self.service.get_all()
        assert len(tasks) == 3
    
    def test_get_all_returns_task_objects(self):
        """Returns list of TodoTask objects."""
        self.service.create(title="Test")
        tasks = self.service.get_all()
        
        from retro_todo.models.todo import TodoTask
        assert all(isinstance(t, TodoTask) for t in tasks)


class TestTodoServiceComplete:
    """Tests for TodoService.complete() - T040."""
    
    @pytest.fixture(autouse=True)
    def setup_service(self, temp_db_path):
        """Initialize database before each test."""
        init_database(temp_db_path)
        self.service = TodoService()
        yield
        close_database()
    
    def test_complete_changes_status(self):
        """complete() sets task status to COMPLETED."""
        task = self.service.create(title="To complete")
        
        completed = self.service.complete(task.id)
        assert completed.status == Status.COMPLETED
    
    def test_complete_sets_completed_at(self):
        """complete() sets completed_at timestamp."""
        task = self.service.create(title="To complete")
        
        completed = self.service.complete(task.id)
        assert completed.completed_at is not None
    
    def test_complete_persists_change(self):
        """Completion persists in database."""
        task = self.service.create(title="To complete")
        self.service.complete(task.id)
        
        retrieved = self.service.get_by_id(task.id)
        assert retrieved.status == Status.COMPLETED
    
    def test_complete_returns_none_for_invalid_id(self):
        """Returns None for nonexistent task."""
        result = self.service.complete(999)
        assert result is None


class TestTodoServiceUpdate:
    """Tests for TodoService.update() - T086."""
    
    @pytest.fixture(autouse=True)
    def setup_service(self, temp_db_path):
        """Initialize database before each test."""
        init_database(temp_db_path)
        self.service = TodoService()
        yield
        close_database()
    
    def test_update_title(self):
        """Can update task title."""
        task = self.service.create(title="Original")
        
        updated = self.service.update(task.id, title="Updated")
        assert updated.title == "Updated"
    
    def test_update_priority(self):
        """Can update task priority."""
        task = self.service.create(title="Test", priority=Priority.LOW)
        
        updated = self.service.update(task.id, priority=Priority.URGENT)
        assert updated.priority == Priority.URGENT
    
    def test_update_persists(self):
        """Update persists in database."""
        task = self.service.create(title="Original")
        self.service.update(task.id, title="Updated")
        
        retrieved = self.service.get_by_id(task.id)
        assert retrieved.title == "Updated"


class TestTodoServiceDelete:
    """Tests for TodoService.delete() - T088."""
    
    @pytest.fixture(autouse=True)
    def setup_service(self, temp_db_path):
        """Initialize database before each test."""
        init_database(temp_db_path)
        self.service = TodoService()
        yield
        close_database()
    
    def test_delete_removes_task(self):
        """delete() removes task from database."""
        task = self.service.create(title="To delete")
        
        result = self.service.delete(task.id)
        assert result is True
        
        retrieved = self.service.get_by_id(task.id)
        assert retrieved is None
    
    def test_delete_returns_false_for_invalid_id(self):
        """delete() returns False for nonexistent task."""
        result = self.service.delete(999)
        assert result is False


class TestTodoServiceStatistics:
    """Tests for TodoService.get_statistics() - T060."""
    
    @pytest.fixture(autouse=True)
    def setup_service(self, temp_db_path):
        """Initialize database before each test."""
        init_database(temp_db_path)
        self.service = TodoService()
        yield
        close_database()
    
    def test_statistics_returns_dict(self):
        """get_statistics() returns a dictionary."""
        stats = self.service.get_statistics()
        assert isinstance(stats, dict)
    
    def test_statistics_counts_total(self):
        """Statistics includes total task count."""
        self.service.create(title="Task 1")
        self.service.create(title="Task 2")
        
        stats = self.service.get_statistics()
        assert stats["total"] == 2
    
    def test_statistics_counts_by_status(self):
        """Statistics includes status breakdown."""
        task = self.service.create(title="Task 1")
        self.service.create(title="Task 2")
        self.service.complete(task.id)
        
        stats = self.service.get_statistics()
        assert stats["completed"] == 1
        assert stats["pending"] == 1
    
    def test_statistics_counts_by_priority(self):
        """Statistics includes priority breakdown."""
        self.service.create(title="Low", priority=Priority.LOW)
        self.service.create(title="High", priority=Priority.HIGH)
        self.service.create(title="High 2", priority=Priority.HIGH)
        
        stats = self.service.get_statistics()
        assert stats["by_priority"]["low"] == 1
        assert stats["by_priority"]["high"] == 2
