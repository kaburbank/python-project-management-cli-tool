# Test user, project, and task creation and relationships
import unittest
import os
import json
from storage.storage import Storage

USER_FILE = os.path.join(os.path.dirname(__file__), '../storage/users.json')
PROJECT_FILE = os.path.join(os.path.dirname(__file__), '../storage/projects.json')
TASK_FILE = os.path.join(os.path.dirname(__file__), '../storage/tasks.json')

class TestPersistence(unittest.TestCase):
    def setUp(self):
        # Clean up files before each test
        for f in [USER_FILE, PROJECT_FILE, TASK_FILE]:
            if os.path.exists(f):
                os.remove(f)
        self.user_storage = Storage(USER_FILE)
        self.project_storage = Storage(PROJECT_FILE)
        self.task_storage = Storage(TASK_FILE)

    def test_user_project_task_flow(self):
        users = {}
        projects = {}
        tasks = {}
        # Add user
        users['1'] = {"user_id": '1', "name": "Alice", "email": "alice@example.com", "projects": []}
        self.user_storage.save(users)
        # Add project
        projects['1'] = {"project_id": '1', "name": "Proj1", "description": "desc", "owner_id": '1', "tasks": [], "contributors": ['1']}
        users['1']['projects'].append('1')
        self.user_storage.save(users)
        self.project_storage.save(projects)
        # Add task
        tasks['1'] = {"task_id": '1', "title": "Task1", "due_date": None, "assigned_to": '1', "status": "pending", "project_id": '1'}
        projects['1']['tasks'].append('1')
        self.project_storage.save(projects)
        self.task_storage.save(tasks)
        # Reload and check
        loaded_users = self.user_storage.load()
        loaded_projects = self.project_storage.load()
        loaded_tasks = self.task_storage.load()
        self.assertIn('1', loaded_users)
        self.assertIn('1', loaded_projects)
        self.assertIn('1', loaded_tasks)
        self.assertIn('1', loaded_users['1']['projects'])
        self.assertIn('1', loaded_projects['1']['tasks'])
        self.assertEqual(loaded_tasks['1']['assigned_to'], '1')

if __name__ == "__main__":
    unittest.main()
