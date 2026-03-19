
"""
Main CLI logic for the Project Management Tool.

This script provides a command-line interface (CLI) for managing users, projects, and tasks.
It supports adding, listing, and updating users, projects, and tasks, and persists data in JSON files.
"""

import os
import sys
import argparse
import logging
from typing import Dict, List
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt

# Ensure the project root is in sys.path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, os.pardir))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from models.entities import User, Project, Task
from storage.storage import Storage
from utils.helpers import validate_email, parse_due_date

def get_next_id(data_dict):
    """
    Get the next available integer ID as a string for a given dictionary.
    Args:
        data_dict (dict): Dictionary with integer string keys
    Returns:
        str: Next available ID
    """
    return str(max([int(k) for k in data_dict.keys()] + [0]) + 1)

# Setup basic logging
"""
Setup basic logging for the CLI.
"""
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(name)s %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger("cli")

# Data file paths
"""
Data file paths for persistent storage.
"""
USER_FILE = os.path.join(os.path.dirname(__file__), '../storage/users.json')
PROJECT_FILE = os.path.join(os.path.dirname(__file__), '../storage/projects.json')
TASK_FILE = os.path.join(os.path.dirname(__file__), '../storage/tasks.json')

user_storage = Storage(USER_FILE)
project_storage = Storage(PROJECT_FILE)
task_storage = Storage(TASK_FILE)

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




console = Console()
parser = argparse.ArgumentParser(description="Project Management CLI Tool")
subparsers = parser.add_subparsers(dest="command")

# Add user
# Command: Add a new user
add_user_parser = subparsers.add_parser("add-user", help="Add a new user")
add_user_parser.add_argument("--name", required=True, help="User name")
add_user_parser.add_argument("--email", required=True, help="User email")

# List users
# Command: List all users
list_user_parser = subparsers.add_parser("list-users", help="List all users")

# Add project
# Command: Add a new project
add_project_parser = subparsers.add_parser("add-project", help="Add a new project")
add_project_parser.add_argument("--user", required=True, help="User name (owner)")
add_project_parser.add_argument("--title", required=True, help="Project title")
add_project_parser.add_argument("--description", default="", help="Project description")

# List projects
# Command: List all projects for a user
list_project_parser = subparsers.add_parser("list-projects", help="List projects for a user")
list_project_parser.add_argument("--user", required=True, help="User name")

# Add task
# Command: Add a new task to a project
add_task_parser = subparsers.add_parser("add-task", help="Add a new task to a project")
add_task_parser.add_argument("--project", required=True, help="Project title")
add_task_parser.add_argument("--title", required=True, help="Task title")
add_task_parser.add_argument("--due", default="", help="Due date (YYYY-MM-DD)")
add_task_parser.add_argument("--user", required=True, help="User name to assign task to")

# List tasks
# Command: List all tasks for a project
list_task_parser = subparsers.add_parser("list-tasks", help="List tasks for a project")
list_task_parser.add_argument("--project", required=True, help="Project title")

# Complete task
# Command: Mark a task as complete
complete_task_parser = subparsers.add_parser("complete-task", help="Mark a task as complete")
complete_task_parser.add_argument("--task", required=True, help="Task title")
complete_task_parser.add_argument("--project", required=True, help="Project title")

args = parser.parse_args()
users, projects, tasks = load_all()


# Helper function to find a user by name
def find_user_by_name(name):
    """
    Find a user dictionary by user name.
    Args:
        name (str): User name
    Returns:
        dict or None: User dict if found, else None
    """
    for u in users.values():
        if u["name"] == name:
            return u
    return None

# Helper function to find a project by title
def find_project_by_title(title):
    """
    Find a project dictionary by project title.
    Args:
        title (str): Project title
    Returns:
        dict or None: Project dict if found, else None
    """
    for p in projects.values():
        if p["name"] == title:
            return p
    return None

# Helper function to find a task by title and project
def find_task_by_title_and_project(task_title, project):
    """
    Find a task dictionary by title within a given project.
    Args:
        task_title (str): Task title
        project (dict): Project dict
    Returns:
        dict or None: Task dict if found, else None
    """
    for tid in project["tasks"]:
        t = tasks.get(tid)
        if t and t["title"] == task_title:
            return t
    return None

# === Main command dispatch block ===
if __name__ == "__main__":
    if args.command == "add-user":
        logger.info(f"Attempting to add user: {args.name} <{args.email}>")
        if not validate_email(args.email):
            logger.error(f"Invalid email: {args.email}")
            console.print(f"[red]Invalid email: '{args.email}'. Please provide a valid email address (e.g., user@example.com).[/red]")
            sys.exit(1)
        # Check for duplicate user name
        if any(u["name"] == args.name for u in users.values()):
            logger.error(f"Duplicate user name: {args.name}")
            console.print(f"[red]A user with the name '{args.name}' already exists. Please choose a different name.[/red]")
            sys.exit(1)
        user_id = get_next_id(users)
        users[user_id] = {"user_id": user_id, "name": args.name, "email": args.email, "projects": []}
        save_all(users, projects, tasks)
        logger.info(f"User '{args.name}' added with ID {user_id}")
        console.print(f"[green]User '{args.name}' added with ID {user_id}.[/green]")

    elif args.command == "list-users":
        table = Table(title="Users")
        table.add_column("ID")
        table.add_column("Name")
        table.add_column("Email")
        for u in users.values():
            table.add_row(u["user_id"], u["name"], u["email"])
        console.print(table)

    elif args.command == "add-project":
        logger.info(f"Attempting to add project: {args.title} for user {args.user}")
        user = find_user_by_name(args.user)
        if not user:
            logger.error(f"User not found: {args.user}")
            console.print(f"[red]User '{args.user}' not found. Please check the user name or add the user first using 'add-user'.[/red]")
            sys.exit(1)
        # Check for duplicate project title
        if any(p["name"] == args.title for p in projects.values()):
            logger.error(f"Duplicate project title: {args.title}")
            console.print(f"[red]A project with the title '{args.title}' already exists. Please choose a different title.[/red]")
            sys.exit(1)
        project_id = get_next_id(projects)
        projects[project_id] = {"project_id": project_id, "name": args.title, "description": args.description, "owner_id": user["user_id"], "tasks": [], "contributors": [user["user_id"]]}
        user["projects"].append(project_id)
        save_all(users, projects, tasks)
        logger.info(f"Project '{args.title}' added for user '{args.user}'")
        console.print(f"[green]Project '{args.title}' added for user '{args.user}'.[/green]")

    elif args.command == "list-projects":
        user = find_user_by_name(args.user)
        if not user:
            console.print(f"[red]User '{args.user}' not found. Please check the user name or add the user first using 'add-user'.[/red]")
            sys.exit(1)
        table = Table(title=f"Projects for {args.user}")
        table.add_column("ID")
        table.add_column("Name")
        table.add_column("Description")
        for pid in user["projects"]:
            p = projects.get(pid)
            if p:
                table.add_row(p["project_id"], p["name"], p["description"])
        console.print(table)

    elif args.command == "add-task":
        logger.info(f"Attempting to add task: {args.title} to project {args.project} for user {args.user}")
        project = find_project_by_title(args.project)
        if not project:
            logger.error(f"Project not found: {args.project}")
            console.print(f"[red]Project '{args.project}' not found. Please check the project title or add the project first using 'add-project'.[/red]")
            sys.exit(1)
        user = find_user_by_name(args.user)
        if not user:
            logger.error(f"User not found: {args.user}")
            console.print(f"[red]User '{args.user}' not found. Please check the user name or add the user first using 'add-user'.[/red]")
            sys.exit(1)
        # Check for duplicate task title in the same project
        if any(tasks[tid]["title"] == args.title for tid in project["tasks"] if tid in tasks):
            logger.error(f"Duplicate task title: {args.title} in project {args.project}")
            console.print(f"[red]A task with the title '{args.title}' already exists in project '{args.project}'. Please choose a different title.[/red]")
            sys.exit(1)
        due_date = parse_due_date(args.due) if args.due else None
        task_id = get_next_id(tasks)
        tasks[task_id] = {"task_id": task_id, "title": args.title, "due_date": due_date.isoformat() if due_date else None, "assigned_to": user["user_id"], "status": "pending", "project_id": project["project_id"]}
        project["tasks"].append(task_id)
        if user["user_id"] not in project["contributors"]:
            project["contributors"].append(user["user_id"])
        save_all(users, projects, tasks)
        logger.info(f"Task '{args.title}' added to project '{args.project}' and assigned to '{args.user}'")
        console.print(f"[green]Task '{args.title}' added to project '{args.project}' and assigned to '{args.user}'.[/green]")

    elif args.command == "list-tasks":
        project = find_project_by_title(args.project)
        if not project:
            console.print(f"[red]Project '{args.project}' not found. Please check the project title or add the project first using 'add-project'.[/red]")
            sys.exit(1)
        table = Table(title=f"Tasks for Project {args.project}")
        table.add_column("ID")
        table.add_column("Title")
        table.add_column("Due Date")
        table.add_column("Assigned To")
        table.add_column("Status")
        for tid in project["tasks"]:
            t = tasks.get(tid)
            if t:
                assigned_user = users.get(t["assigned_to"], {}).get("name", t["assigned_to"])
                table.add_row(t["task_id"], t["title"], t["due_date"] or "", assigned_user, t["status"])
        console.print(table)

    elif args.command == "complete-task":
        logger.info(f"Attempting to complete task: {args.task} in project {args.project}")
        project = find_project_by_title(args.project)
        if not project:
            logger.error(f"Project not found: {args.project}")
            console.print(f"[red]Project '{args.project}' not found. Please check the project title or add the project first using 'add-project'.[/red]")
            sys.exit(1)
        task = find_task_by_title_and_project(args.task, project)
        if not task:
            logger.error(f"Task not found: {args.task} in project {args.project}")
            console.print(f"[red]Task '{args.task}' not found in project '{args.project}'. Please check the task title or add the task first using 'add-task'.[/red]")
            sys.exit(1)
        task["status"] = "complete"
        save_all(users, projects, tasks)
        logger.info(f"Task '{args.task}' marked as complete in project '{args.project}'")
        console.print(f"[green]Task '{args.task}' marked as complete in project '{args.project}'.[/green]")

    else:
        parser.print_help()
