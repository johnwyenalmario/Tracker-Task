#!/usr/bin/env python3

import os
import sys
import json
import subprocess
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
        'createdAt': date,
        'updatedAt': date
    }
    tasks.append(task)
    save_tasks(tasks)
    print(f'Task created successfully id:{new_id}')

def update_tasks(task_id, description):
    tasks = load_tasks()
    found = False
    for t in tasks:
        if t['id'] == int(task_id):
            t['description'] = description
            t['updatedAt'] = datetime.now().isoformat()
            save_tasks(tasks)
            print('Task Saved Successfully.')
            found = True
            break
    if not found:
        print('Task not found.')

def delete_tasks(task_id):
    tasks = load_tasks()
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
    for t in tasks:
        if t['id'] == int(task_id):
            t['status'] = status
            t['updatedAt'] = datetime.now().isoformat()
            save_tasks(tasks)
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
        print(f"[{t['id']}] {t['description']} - {t['status']} (Created: {t['createdAt']})")

def main(): 
    if len(sys.argv) < 2:
        print('Usage: task [add|update|delete|mark-in-progress|mark-done|list|install]')
        return

    command = sys.argv[1]

    # --- SELF INSTALLATION SYSTEM ---
    if command == 'install':
        script_path = os.path.abspath(sys.argv[0])
        symlink_path = '/usr/local/bin/task'

        print("Setting up 'task' as a system-wide command...")
        try:
            # 1. Make the script executable (chmod +x)
            os.chmod(script_path, 0o755)

            # 2. Check if symlink already exists
            if os.path.exists(symlink_path) or os.path.islink(symlink_path):
                print(f"Error: {symlink_path} already exists. Uninstalling old link...")
                subprocess.run(['sudo', 'rm', symlink_path], check=True)

            # 3. Create the symlink using sudo since /usr/local/bin requires root
            print("Creating system symlink (you may be prompted for your sudo password):")
            subprocess.run(['sudo', 'ln', '-s', script_path, symlink_path], check=True)
            
            print("\nInstallation successful! You can now use the 'task' command anywhere.")
        except subprocess.CalledProcessError:
            print("\nInstallation failed: Sudo permissions were denied or interrupted.")
        except Exception as e:
            print(f"\nAn error occurred during installation: {e}")
        return

    # --- TASK COMMANDS ---
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