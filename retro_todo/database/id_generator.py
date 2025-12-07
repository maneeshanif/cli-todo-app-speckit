"""
Atomic ID generator for task identification.

Ensures unique task IDs without collisions.

T025: GREEN phase implementation.
"""
from typing import List, Dict, Any


def generate_task_id(existing_tasks: List[Dict[str, Any]]) -> int:
    """
    Generate next available task ID.
    
    Args:
        existing_tasks: List of existing task dictionaries with 'id' field
        
    Returns:
        Next available integer ID (max existing + 1, or 1 if empty)
    """
    if not existing_tasks:
        return 1
    return max(task['id'] for task in existing_tasks) + 1
