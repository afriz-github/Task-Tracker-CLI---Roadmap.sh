import argparse
import json
import os
from datetime import datetime

DATA_FILE = "tasks.json"

def load_tasks():
    if not os.path.exists(DATA_FILE):
        return []
    
    with open(DATA_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_tasks(tasks):
    with open(DATA_FILE, "w") as f:
        json.dump(tasks, f, indent=2)

def add_task(description):
    tasks = load_tasks()
    new_id = max([t["id"] for t in tasks], default=0) + 1
    timestamp = datetime.now().isoformat()
    
    new_task = {
        "id": new_id,
        "description": description,
        "status": "todo",
        "createdAt": timestamp,
        "updatedAt": timestamp
    }
    
    tasks.append(new_task)
    save_tasks(tasks)
    print(f"Task added successfully (ID: {new_id})")

def update_task(task_id, new_description):
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            task["description"] = new_description
            task["updatedAt"] = datetime.now().isoformat()
            save_tasks(tasks)
            print(f"Task {task_id} updated successfully")
            return
    print(f"Error: Task with ID {task_id} not found")

def delete_task(task_id):
    tasks = load_tasks()
    filtered = [t for t in tasks if t["id"] != task_id]
    
    if len(filtered) == len(tasks):
        print(f"Error: Task with ID {task_id} not found")
        return
    
    save_tasks(filtered)
    print(f"Task {task_id} deleted successfully")

def mark_task(task_id, new_status):
    valid_statuses = ["todo", "in-progress", "done"]
    if new_status not in valid_statuses:
        print(f"Error: Invalid status. Use {', '.join(valid_statuses)}")
        return

    tasks = load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            task["status"] = new_status
            task["updatedAt"] = datetime.now().isoformat()
            save_tasks(tasks)
            print(f"Task {task_id} marked as {new_status}")
            return
    print(f"Error: Task with ID {task_id} not found")

def list_tasks(status_filter=None):
    tasks = load_tasks()
    
    if status_filter:
        valid_statuses = ["todo", "in-progress", "done"]
        if status_filter not in valid_statuses:
            print(f"Error: Invalid filter. Use {', '.join(valid_statuses)}")
            return
            
        tasks = [t for t in tasks if t["status"] == status_filter]
    
    if not tasks:
        print("No tasks found")
        return
    
    print(f"{'ID':<5} {'Status':<12} {'Description':<40} {'Created':<20} {'Updated':<20}")
    print("-" * 95)
    for task in tasks:
        print(f"{task['id']:<5} {task['status']:<12} {task['description'][:35]:<40} {task['createdAt'][:16]:<20} {task['updatedAt'][:16]:<20}")

def main():
    parser = argparse.ArgumentParser(description="Task Tracker CLI")
    subparsers = parser.add_subparsers(dest="command")

    # Add command
    add_parser = subparsers.add_parser("add")
    add_parser.add_argument("description", type=str)

    # Update command
    update_parser = subparsers.add_parser("update")
    update_parser.add_argument("task_id", type=int)
    update_parser.add_argument("new_description", type=str)

    # Delete command
    delete_parser = subparsers.add_parser("delete")
    delete_parser.add_argument("task_id", type=int)

    # Mark commands
    mark_parser = subparsers.add_parser("mark-done")
    mark_parser.add_argument("task_id", type=int)
    
    mark_parser = subparsers.add_parser("mark-in-progress")
    mark_parser.add_argument("task_id", type=int)

    # List command
    list_parser = subparsers.add_parser("list")
    list_parser.add_argument("status_filter", nargs="?", default=None)

    args = parser.parse_args()

    if args.command == "add":
        add_task(args.description)
    elif args.command == "update":
        update_task(args.task_id, args.new_description)
    elif args.command == "delete":
        delete_task(args.task_id)
    elif args.command == "mark-done":
        mark_task(args.task_id, "done")
    elif args.command == "mark-in-progress":
        mark_task(args.task_id, "in-progress")
    elif args.command == "list":
        list_tasks(args.status_filter)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()