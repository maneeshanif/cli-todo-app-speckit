"""
TinyDB database wrapper with CachingMiddleware.

Provides database initialization and CRUD operations for TodoTask persistence.

T023, T027: GREEN phase implementation.
"""
import os
from typing import Optional, List

from tinydb import TinyDB, Query
from tinydb.middlewares import CachingMiddleware
from tinydb.storages import JSONStorage

from retro_todo.models.todo import TodoTask
from .id_generator import generate_task_id


# Module-level database instance (singleton pattern)
_db: Optional[TinyDB] = None
_tasks_table = None
_db_path: str = "todo_data.json"


def init_database(db_path: Optional[str] = None) -> TinyDB:
    """
    Initialize database with CachingMiddleware for performance.
    
    Args:
        db_path: Path to database file. Uses default if not provided.
        
    Returns:
        TinyDB instance
    """
    global _db, _tasks_table, _db_path
    
    if db_path:
        _db_path = db_path
    
    if _db is not None:
        close_database()
    
    _db = TinyDB(
        _db_path,
        storage=CachingMiddleware(JSONStorage),
        indent=2,
        ensure_ascii=False
    )
    _tasks_table = _db.table('tasks')
    
    return _db


def get_database() -> TinyDB:
    """Get database instance, initializing if needed."""
    global _db
    if _db is None:
        init_database()
    return _db


def get_tasks_table():
    """Get tasks table, initializing database if needed."""
    global _tasks_table
    if _tasks_table is None:
        init_database()
    return _tasks_table


def close_database() -> None:
    """Close database connection and flush cache."""
    global _db, _tasks_table
    if _db is not None:
        _db.close()
        _db = None
        _tasks_table = None


# CRUD Operations

def insert_task(task: TodoTask) -> int:
    """
    Insert a new task into the database.
    
    Args:
        task: TodoTask instance to insert
        
    Returns:
        Document ID from TinyDB
    """
    table = get_tasks_table()
    return table.insert(task.to_dict())


def get_task(task_id: int) -> Optional[TodoTask]:
    """
    Retrieve a task by ID.
    
    Args:
        task_id: Task ID to search for
        
    Returns:
        TodoTask instance or None if not found
    """
    table = get_tasks_table()
    Task = Query()
    result = table.search(Task.id == task_id)
    
    if not result:
        return None
    
    return TodoTask.from_dict(result[0])


def get_all_tasks() -> List[TodoTask]:
    """
    Retrieve all tasks from the database.
    
    Returns:
        List of TodoTask instances
    """
    table = get_tasks_table()
    return [TodoTask.from_dict(doc) for doc in table.all()]


def update_task(task: TodoTask) -> bool:
    """
    Update an existing task in the database.
    
    Args:
        task: TodoTask instance with updated data
        
    Returns:
        True if task was updated, False otherwise
    """
    table = get_tasks_table()
    Task = Query()
    result = table.update(task.to_dict(), Task.id == task.id)
    return len(result) > 0


def delete_task(task_id: int) -> bool:
    """
    Delete a task from the database.
    
    Args:
        task_id: ID of task to delete
        
    Returns:
        True if task was deleted, False otherwise
    """
    table = get_tasks_table()
    Task = Query()
    result = table.remove(Task.id == task_id)
    return len(result) > 0


def get_next_task_id() -> int:
    """
    Generate the next available task ID.
    
    Returns:
        Next available integer ID
    """
    table = get_tasks_table()
    return generate_task_id(table.all())
