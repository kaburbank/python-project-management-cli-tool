


import argparse
import os
from utils.data_access import ensure_data_dir, load_all, save_all
from rich.console import Console
from rich.table import Table
from datetime import datetime

DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
USER_FILE = os.path.join(DATA_DIR, 'users.json')
PROJECT_FILE = os.path.join(DATA_DIR, 'projects.json')
TASK_FILE = os.path.join(DATA_DIR, 'tasks.json')

console = Console()

def get_next_id(data_dict):
    """
    Get the next available integer ID for a dictionary of items.
    Args:
        data_dict (dict): Dictionary with integer keys as strings.
    Returns:
        str: Next available ID as a string.
    """
    return str(max([int(k) for k in data_dict.keys()] + [0]) + 1)

class Person:
    def __init__(self, name: str):
        """
        Initialize a Person with a name.
        Args:
            name (str): The person's name.
        """
        self.name = name

class User(Person):
    id_counter = 1
    def __init__(self, name: str, email: str, user_id=None):
        """
        Initialize a User with name, email, and optional user_id.
        Args:
            name (str): User's name.
            email (str): User's email.
            user_id (int, optional): User ID. If None, auto-incremented.
        """
        super().__init__(name)
        self.email = email
        self.projects = []
        if user_id is None:
            self.user_id = User.id_counter
            User.id_counter += 1
        else:
            self.user_id = int(user_id)

    @property
    def email(self):
        """
        Get the user's email address.
        Returns:
            str: The email address.
        """
        return self._email
    @email.setter
    def email(self, value):
        """
        Set the user's email address, validating format.
        Args:
            value (str): The email address to set.
        Raises:
            ValueError: If email is invalid.
        """
        if '@' not in value:
            raise ValueError('Invalid email')
        self._email = value
    def __str__(self):
        """
        String representation of the User.
        Returns:
            str: User info string.
        """
        return f"User({self.user_id}): {self.name} <{self.email}>"

class Project:
    id_counter = 1
    def __init__(self, title: str, description: str, due_date: str, owner_id: int, project_id=None):
        """
        Initialize a Project with title, description, due date, owner, and optional project_id.
        Args:
            title (str): Project title.
            description (str): Project description.
            due_date (str): Due date string.
            owner_id (int): Owner user ID.
            project_id (int, optional): Project ID. If None, auto-incremented.
        """
        self.title = title
        self.description = description
        self.due_date = due_date
        self.owner_id = owner_id
        self.tasks = []
        if project_id is None:
            self.project_id = Project.id_counter
            Project.id_counter += 1
        else:
            self.project_id = int(project_id)
    def __str__(self):
        """
        String representation of the Project.
        Returns:
            str: Project info string.
        """
        return f"Project({self.project_id}): {self.title} (Due: {self.due_date})"

class Task:
    id_counter = 1
    def __init__(self, title: str, status: str, assigned_to: int, task_id=None):
        """
        Initialize a Task with title, status, assigned user, and optional task_id.
        Args:
            title (str): Task title.
            status (str): Task status.
            assigned_to (int): User ID assigned to task.
            task_id (int, optional): Task ID. If None, auto-incremented.
        """
        self.title = title
        self.status = status
        self.assigned_to = assigned_to
        if task_id is None:
            self.task_id = Task.id_counter
            Task.id_counter += 1
        else:
            self.task_id = int(task_id)
    def __str__(self):
        """
        String representation of the Task.
        Returns:
            str: Task info string.
        """
        return f"Task({self.task_id}): {self.title} [{self.status}]"

def main():
    ensure_data_dir()
    parser = argparse.ArgumentParser(description="Project Management CLI Tool")
    subparsers = parser.add_subparsers(dest="command")

    # Add user
    add_user_parser = subparsers.add_parser("add-user", help="Add a new user")
    add_user_parser.add_argument("--name", required=True, help="User name")
    add_user_parser.add_argument("--email", required=True, help="User email")

    # List projects
    list_projects_parser = subparsers.add_parser("list-projects", help="List all projects")

    # Add project
    add_project_parser = subparsers.add_parser("add-project", help="Add a new project")
    add_project_parser.add_argument("--user", required=True, help="User name (owner)")
    add_project_parser.add_argument("--title", required=True, help="Project title")
    add_project_parser.add_argument("--description", default="", help="Project description")
    add_project_parser.add_argument("--due_date", default="", help="Due date (YYYY-MM-DD)")

    # Add task
    add_task_parser = subparsers.add_parser("add-task", help="Add a new task to a project")
    add_task_parser.add_argument("--project", required=True, help="Project title")
    add_task_parser.add_argument("--title", required=True, help="Task title")
    add_task_parser.add_argument("--user", required=True, help="User name to assign task to")
    add_task_parser.add_argument("--status", default="pending", help="Task status")

    # List tasks
    list_task_parser = subparsers.add_parser("list-tasks", help="List tasks for a project")
    list_task_parser.add_argument("--project", required=True, help="Project title")

    # Complete task
    complete_task_parser = subparsers.add_parser("complete-task", help="Mark a task as complete")
    complete_task_parser.add_argument("--project", required=True, help="Project title")
    complete_task_parser.add_argument("--task", required=True, help="Task title")

    args = parser.parse_args()
    users, projects, tasks = load_all()

    # Helper functions
    def find_user_by_name(name):
        for u in users.values():
            if u["name"] == name:
                return u
        return None
    def find_project_by_title(title):
        for p in projects.values():
            if p["title"] == title:
                return p
        return None
    def find_task_by_title_and_project(task_title, project):
        for tid in project["tasks"]:
            t = tasks.get(str(tid))
            if t and t["title"] == task_title:
                return t
        return None

    if args.command == "add-user":
        # Enforce unique user names
        if any(u["name"] == args.name for u in users.values()):
            console.print(f"[red]A user with the name '{args.name}' already exists. Please choose a different name.[/red]")
            return
        user_id = get_next_id(users)
        try:
            user = User(args.name, args.email, user_id)
        except ValueError as e:
            console.print(f"[red]{e}[/red]")
            return
        users[user_id] = {"user_id": user.user_id, "name": user.name, "email": user.email, "projects": []}
        save_all(users, projects, tasks)
        console.print(f"[green]{user} added.[/green]")

    elif args.command == "add-project":
        user = find_user_by_name(args.user)
        if not user:
            console.print("[red]User not found.[/red]")
            return
        project_id = get_next_id(projects)
        project = Project(args.title, args.description, args.due_date, user["user_id"], project_id)
        projects[project_id] = {"project_id": project.project_id, "title": project.title, "description": project.description, "due_date": project.due_date, "owner_id": project.owner_id, "tasks": []}
        user["projects"].append(project_id)
        save_all(users, projects, tasks)
        console.print(f"[green]{project} added for user '{args.user}'.[/green]")

    elif args.command == "add-task":
        project = find_project_by_title(args.project)
        if not project:
            console.print("[red]Project not found.[/red]")
            return
        user = find_user_by_name(args.user)
        if not user:
            console.print("[red]User not found.[/red]")
            return
        task_id = get_next_id(tasks)
        task = Task(args.title, args.status, user["user_id"], task_id)
        tasks[task_id] = {"task_id": task.task_id, "title": task.title, "status": task.status, "assigned_to": task.assigned_to}
        project["tasks"].append(task_id)
        save_all(users, projects, tasks)
        console.print(f"[green]{task} added to project '{args.project}'.[/green]")


    elif args.command == "list-projects":
        table = Table(title="Projects")
        table.add_column("ID")
        table.add_column("Title")
        table.add_column("Description")
        table.add_column("Due Date")
        table.add_column("Owner")
        for p in projects.values():
            owner = users.get(str(p["owner_id"]), {}).get("name", str(p["owner_id"]))
            table.add_row(str(p["project_id"]), p["title"], p["description"], p["due_date"], owner)
        console.print(table)

    elif args.command == "list-tasks":
        project = find_project_by_title(args.project)
        if not project:
            console.print(f"[red]Project '{args.project}' not found. Please check the project title or add the project first using 'add-project'.[/red]")
            return
        table = Table(title=f"Tasks for Project {args.project}")
        table.add_column("ID")
        table.add_column("Title")
        table.add_column("Due Date")
        table.add_column("Assigned To")
        table.add_column("Status")
        for tid in project["tasks"]:
            t = tasks.get(str(tid))
            if t:
                assigned_user = users.get(str(t["assigned_to"]), {}).get("name", str(t["assigned_to"]))
                table.add_row(str(t["task_id"]), t["title"], t.get("due_date", "") or "", assigned_user, t["status"])
        console.print(table)

    elif args.command == "complete-task":
        project = find_project_by_title(args.project)
        if not project:
            console.print("[red]Project not found.[/red]")
            return
        task = find_task_by_title_and_project(args.task, project)
        if not task:
            console.print("[red]Task not found in project.[/red]")
            return
        task["status"] = "complete"
        save_all(users, projects, tasks)
        console.print(f"[green]Task '{args.task}' marked as complete in project '{args.project}'.[/green]")

    else:
        parser.print_help()

if __name__ == "__main__":
    main()
