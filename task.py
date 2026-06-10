import os
import sys
import json
from datetime import datetime

FILE_NAME = 'task.json'

def load_tasks():
    if not os.path.exists(FILE_NAME):
        return []
    with open(FILE_NAME, 'r') as f: 
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_tasks(tasks):
    with open(FILE_NAME, 'w') as f:
        json.dump(tasks, f, indent=4)

def add_tasks(description):
    tasks = load_tasks()
    new_id = max([t['id'] for t in tasks], default=0) + 1
    date = datetime.now().isoformat()
    task = {
        'id': new_id,
        'description': description,
        'status': 'todo',
        'createdAt': date,  # Standardized casing
        'updatedAt': date
    }
    tasks.append(task)  # Fixed: appended 'task', not 'tasks'
    save_tasks(tasks)
    print(f'Task created successfully id:{new_id}')

def update_tasks(task_id, description):
    tasks = load_tasks()
    found = False
    for t in tasks:  # Fixed: changed 'task' to 'tasks'
        if t['id'] == int(task_id):
            t['description'] = description
            t['updatedAt'] = datetime.now().isoformat()  # Fixed: datetime usage
            save_tasks(tasks)  # Fixed: function name
            print('Task Saved Successfully.')
            found = True
            break
    if not found:
        print('Task not found.')

def delete_tasks(task_id):
    tasks = load_tasks()  # Fixed: function name
    initial_length = len(tasks)
    tasks = [t for t in tasks if t['id'] != int(task_id)]
    
    if len(tasks) == initial_length:
        print('Task not found.')
    else:
        save_tasks(tasks)
        print('Task deleted successfully')

def mark_tasks(task_id, status):
    tasks = load_tasks()
    found = False
    for t in tasks:  # Fixed: changed 'task' to 'tasks'
        if t['id'] == int(task_id):
            t['status'] = status
            t['updatedAt'] = datetime.now().isoformat()  # Fixed: datetime usage
            save_tasks(tasks)  # Fixed: function name
            print(f'Task {task_id} marked as {status}.')
            found = True
            break
    if not found:
        print('Task not found.')

def list_tasks(status=None):
    tasks = load_tasks()
    if status:
        tasks = [t for t in tasks if t['status'] == status]
    
    if not tasks:
        print('No tasks found.')
        return

    for t in tasks:
        # Fixed: Adjusted internal quotes and standardized 'createdAt' casing
        print(f"[{t['id']}] {t['description']} - {t['status']} (Created: {t['createdAt']})")

def main(): 
    if len(sys.argv) < 2:
        print('Usage: python task.py [add|update|delete|mark-in-progress|mark-done|list]')
        return

    command = sys.argv[1]

    if command == 'add':
        if len(sys.argv) < 3:
            print("Error: Missing task description.")
            return
        add_tasks(sys.argv[2])
    elif command == 'update':
        if len(sys.argv) < 4:
            print("Error: Missing ID or description.")
            return
        update_tasks(sys.argv[2], sys.argv[3])
    elif command == 'delete':
        if len(sys.argv) < 3:
            print("Error: Missing task ID.")
            return
        delete_tasks(sys.argv[2])
    elif command == 'mark-in-progress':
        if len(sys.argv) < 3:
            print("Error: Missing task ID.")
            return
        mark_tasks(sys.argv[2], 'in-progress')
    elif command == 'mark-done':
        if len(sys.argv) < 3:
            print("Error: Missing task ID.")
            return
        mark_tasks(sys.argv[2], 'done')
    elif command == 'list':
        status = sys.argv[2] if len(sys.argv) > 2 else None
        list_tasks(status)
    else:
        print(f"Unknown command: {command}")

if __name__ == '__main__':
    main()