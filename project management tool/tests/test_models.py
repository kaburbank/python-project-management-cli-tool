import unittest
from models.entities import User, Project, Task
from datetime import datetime

class TestUserProjectTask(unittest.TestCase):
    def test_user_creation(self):
        user = User(user_id=1, name="Alex", email="alex@example.com")
        self.assertEqual(user.name, "Alex")
        self.assertEqual(user.email, "alex@example.com")
        self.assertEqual(user.projects, [])

    def test_project_creation(self):
        project = Project(project_id=1, title="CLI Tool", description="desc", due_date=datetime(2026,3,31), owner_id=1)
        self.assertEqual(project.title, "CLI Tool")
        self.assertEqual(project.description, "desc")
        self.assertEqual(project.due_date, datetime(2026,3,31))
        self.assertEqual(project.owner_id, 1)
        self.assertEqual(project.tasks, [])

    def test_task_creation(self):
        task = Task(task_id=1, title="Implement add-task", status="pending", assigned_to=1)
        self.assertEqual(task.title, "Implement add-task")
        self.assertEqual(task.status, "pending")
        self.assertEqual(task.assigned_to, 1)

if __name__ == "__main__":
    unittest.main()
