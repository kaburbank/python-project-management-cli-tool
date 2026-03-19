# Shared data access and persistence logic for users, projects, and tasks
import os
from storage.storage import Storage

def get_data_dir():
    """
    Return the absolute path to the unified data directory.
    """
    return os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')

USER_FILE = os.path.join(get_data_dir(), 'users.json')
PROJECT_FILE = os.path.join(get_data_dir(), 'projects.json')
TASK_FILE = os.path.join(get_data_dir(), 'tasks.json')

user_storage = Storage(USER_FILE)
project_storage = Storage(PROJECT_FILE)
task_storage = Storage(TASK_FILE)

def ensure_data_dir():
    """
    Ensure the data directory exists. Creates it if missing.
    """
    data_dir = get_data_dir()
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)


def load_all():
    """
    Load all users, projects, and tasks from storage.
    Returns:
        tuple: (users, projects, tasks) dictionaries
    """
    users = user_storage.load()
    projects = project_storage.load()
    tasks = task_storage.load()
    return users, projects, tasks


def save_all(users, projects, tasks):
    """
    Save all users, projects, and tasks to storage.
    Args:
        users (dict): Users data
        projects (dict): Projects data
        tasks (dict): Tasks data
    """
    user_storage.save(users)
    project_storage.save(projects)
    task_storage.save(tasks)
