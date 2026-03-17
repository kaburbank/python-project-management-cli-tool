# User, Project, and Task models
from typing import List, Optional
from datetime import datetime

class User:
    """Represents a user in the project management system."""
    def __init__(self, user_id: int, name: str, email: str):
        """Initialize a User with id, name, and email."""
        self.user_id = user_id
        self.name = name
        self.email = email
        self.projects: List[int] = []  # List of project IDs


class Project:
    """Represents a project owned by a user."""
    def __init__(self, project_id: int, title: str, description: str, due_date: Optional[datetime], owner_id: int):
        """Initialize a Project with id, title, description, due date, and owner."""
        self.project_id = project_id
        self.title = title
        self.description = description
        self.due_date = due_date
        self.owner_id = owner_id
        self.tasks: List[int] = []  # List of task IDs

class Task:
    """Represents a task within a project."""
    def __init__(self, task_id: int, title: str, status: str, assigned_to: int):
        """Initialize a Task with id, title, status, and assigned user."""
        self.task_id = task_id
        self.title = title
        self.status = status
        self.assigned_to = assigned_to
