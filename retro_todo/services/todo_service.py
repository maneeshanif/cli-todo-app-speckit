"""
TodoService - Business logic layer for task management.

Provides CRUD operations, completion workflow, and statistics.

T037, T039, T041, T061, T087, T089: GREEN phase implementation.
"""
from datetime import datetime
from typing import Optional, List, Dict, Any

from retro_todo.database.db import (
    get_next_task_id,
    insert_task,
    get_task,
    get_all_tasks,
    update_task as db_update_task,
    delete_task as db_delete_task
)
from retro_todo.models.todo import TodoTask
from retro_todo.models.enums import Priority, Status, RecurrencePattern


class TodoService:
    """
    Business logic service for todo task management.
    
    Coordinates between the UI layer and database layer,
    providing high-level operations for task lifecycle management.
    """
    
    def create(
        self,
        title: str,
        description: Optional[str] = None,
        priority: Priority = Priority.MEDIUM,
        tags: Optional[List[str]] = None,
        due_date: Optional[datetime] = None,
        recurrence_pattern: RecurrencePattern = RecurrencePattern.NONE
    ) -> TodoTask:
        """
        Create a new task.
        
        Args:
            title: Task title (required)
            description: Optional detailed description
            priority: Task priority level
            tags: List of categorization tags
            due_date: Optional deadline
            recurrence_pattern: Repetition schedule
            
        Returns:
            Created TodoTask instance
        """
        task_id = get_next_task_id()
        
        task = TodoTask(
            id=task_id,
            title=title,
            description=description,
            priority=priority,
            tags=tags or [],
            due_date=due_date,
            recurrence_pattern=recurrence_pattern
        )
        
        insert_task(task)
        return task
    
    def get_by_id(self, task_id: int) -> Optional[TodoTask]:
        """
        Retrieve a task by ID.
        
        Args:
            task_id: Task ID to find
            
        Returns:
            TodoTask if found, None otherwise
        """
        return get_task(task_id)
    
    def get_all(self) -> List[TodoTask]:
        """
        Retrieve all tasks.
        
        Returns:
            List of all TodoTask instances
        """
        return get_all_tasks()
    
    def complete(self, task_id: int) -> Optional[TodoTask]:
        """
        Mark a task as completed.
        
        Args:
            task_id: ID of task to complete
            
        Returns:
            Updated TodoTask or None if not found
        """
        task = get_task(task_id)
        if task is None:
            return None
        
        task.mark_complete()
        db_update_task(task)
        
        return task
    
    def update(
        self,
        task_id: int,
        title: Optional[str] = None,
        description: Optional[str] = None,
        priority: Optional[Priority] = None,
        tags: Optional[List[str]] = None,
        due_date: Optional[datetime] = None,
        recurrence_pattern: Optional[RecurrencePattern] = None
    ) -> Optional[TodoTask]:
        """
        Update an existing task.
        
        Only provided fields are updated.
        
        Args:
            task_id: ID of task to update
            title: New title
            description: New description
            priority: New priority
            tags: New tags (replaces existing)
            due_date: New due date
            recurrence_pattern: New recurrence pattern
            
        Returns:
            Updated TodoTask or None if not found
        """
        task = get_task(task_id)
        if task is None:
            return None
        
        if title is not None:
            task.title = title
        if description is not None:
            task.description = description
        if priority is not None:
            task.priority = priority
        if tags is not None:
            task.tags = tags
        if due_date is not None:
            task.due_date = due_date
        if recurrence_pattern is not None:
            task.recurrence_pattern = recurrence_pattern
        
        task.updated_at = datetime.now()
        db_update_task(task)
        
        return task
    
    def delete(self, task_id: int) -> bool:
        """
        Delete a task.
        
        Args:
            task_id: ID of task to delete
            
        Returns:
            True if deleted, False if not found
        """
        return db_delete_task(task_id)
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get task statistics.
        
        Returns:
            Dictionary with task counts and breakdowns
        """
        tasks = get_all_tasks()
        
        # Count by status
        completed = sum(1 for t in tasks if t.status == Status.COMPLETED)
        pending = sum(1 for t in tasks if t.status == Status.PENDING)
        
        # Count by priority
        by_priority = {}
        for priority in Priority:
            count = sum(1 for t in tasks if t.priority == priority)
            by_priority[priority.value] = count
        
        # Count by tags
        tag_counts = {}
        for task in tasks:
            for tag in task.tags:
                tag_counts[tag] = tag_counts.get(tag, 0) + 1
        
        # Count overdue
        overdue = sum(1 for t in tasks if t.is_overdue())
        
        return {
            "total": len(tasks),
            "completed": completed,
            "pending": pending,
            "overdue": overdue,
            "by_priority": by_priority,
            "by_tags": tag_counts,
        }
    
    def get_pending(self) -> List[TodoTask]:
        """Get all pending tasks."""
        return [t for t in get_all_tasks() if t.status == Status.PENDING]
    
    def get_completed(self) -> List[TodoTask]:
        """Get all completed tasks."""
        return [t for t in get_all_tasks() if t.status == Status.COMPLETED]
    
    def get_overdue(self) -> List[TodoTask]:
        """Get all overdue tasks."""
        return [t for t in get_all_tasks() if t.is_overdue()]
