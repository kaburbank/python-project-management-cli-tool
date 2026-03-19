# Project Management CLI Tool

## Setup Instructions

1. **Clone the repository** and open the project folder in VS Code.
2. **Install dependencies:**
	 ```
	 pip install -r requirements.txt
	 ```
3. **(Optional) Create a virtual environment:**
	 ```
	 python -m venv .venv
	 source .venv/bin/activate  # On Windows: .venv\\Scripts\\activate
	 ```

## How to Run CLI Commands

Run the CLI tool using Python:

```
python main.py <command> [options]
```

### Example Commands

- Add a user:
	```
	python main.py add-user --name "Alex" --email "alex@example.com"
	```
- Add a project:
	```
	python main.py add-project --user "Alex" --title "CLI Tool" --description "A CLI app" --due_date "2026-03-31"
	```
- Add a task:
	```
	python main.py add-task --project "CLI Tool" --title "Implement add-task" --user "Alex"
	```
- List all projects:
	```
	python main.py list-projects
	```
- List all tasks for a project:
	```
	python main.py list-tasks --project "CLI Tool"
	```
- Mark a task as complete:
	```
	python main.py complete-task --project "CLI Tool" --task "Implement add-task"
	```

## Features

- Manage users, projects, and tasks from the command line
- One-to-many relationships: Users → Projects, Projects → Tasks
- Data persistence using JSON files in the `data/` directory
- Pretty CLI output using the `rich` package
- Modular code structure for easy maintenance
- Unit tests for models and CLI logic

## Known Issues

- No authentication or user roles (all users are admins)
- No support for deleting users, projects, or tasks
- No advanced search or filtering
- Minimal error handling for malformed data

