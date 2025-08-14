#!/usr/bin/env python3
"""
Simple To-Do List Manager - Easy to understand version
"""

import json
import os

class TodoManager:
    def __init__(self):
        self.tasks = []
        self.load_tasks()
    
    def load_tasks(self):
        """Load tasks from file if it exists"""
        if os.path.exists('tasks.json'):
            try:
                with open('tasks.json', 'r') as f:
                    self.tasks = json.load(f)
            except:
                self.tasks = []
    
    def save_tasks(self):
        """Save tasks to file"""
        with open('tasks.json', 'w') as f:
            json.dump(self.tasks, f, indent=2)
    
    def add_task(self, description):
        """Add a new task"""
        if description.strip():
            task = {
                'id': len(self.tasks) + 1,
                'description': description.strip(),
                'completed': False
            }
            self.tasks.append(task)
            self.save_tasks()
            print(f"✅ Added: {description}")
        else:
            print("❌ Task description cannot be empty!")
    
    def complete_task(self, task_id):
        """Mark task as completed"""
        for task in self.tasks:
            if task['id'] == task_id:
                if not task['completed']:
                    task['completed'] = True
                    self.save_tasks()
                    print(f"✅ Completed: {task['description']}")
                else:
                    print("❌ Task already completed!")
                return
        print("❌ Task not found!")
    
    def delete_task(self, task_id):
        """Delete a task"""
        for i, task in enumerate(self.tasks):
            if task['id'] == task_id:
                deleted_task = self.tasks.pop(i)
                self.save_tasks()
                print(f"🗑️ Deleted: {deleted_task['description']}")
                return
        print("❌ Task not found!")
    
    def list_tasks(self):
        """Show all tasks"""
        if not self.tasks:
            print("📝 No tasks yet! Add some tasks to get started.")
            return
        
        print("\n📋 YOUR TO-DO LIST:")
        print("-" * 40)
        
        pending = [t for t in self.tasks if not t['completed']]
        completed = [t for t in self.tasks if t['completed']]
        
        if pending:
            print("⏳ PENDING:")
            for task in pending:
                print(f"  {task['id']}. {task['description']}")
        
        if completed:
            print("✅ COMPLETED:")
            for task in completed:
                print(f"  {task['id']}. {task['description']}")
        
        print("-" * 40)

def show_help():
    """Show available commands"""
    print("\n🎯 COMMANDS:")
    print("  add <task>       - Add new task")
    print("  list             - Show all tasks")
    print("  done <id>        - Mark task as completed")
    print("  delete <id>      - Delete task")
    print("  help             - Show this help")
    print("  quit             - Exit program\n")

def main():
    """Main program loop"""
    todo = TodoManager()
    
    print("🎯 Simple To-Do Manager")
    print("Type 'help' to see commands\n")
    
    while True:
        try:
            user_input = input("📝 Enter command: ").strip()
            
            if not user_input:
                continue
            
            parts = user_input.split(' ', 1)
            command = parts[0].lower()
            
            if command == 'quit' or command == 'exit':
                print("👋 Goodbye!")
                break
            
            elif command == 'help':
                show_help()
            
            elif command == 'list':
                todo.list_tasks()
            
            elif command == 'add' and len(parts) > 1:
                todo.add_task(parts[1])
            
            elif command == 'done' and len(parts) > 1:
                try:
                    task_id = int(parts[1])
                    todo.complete_task(task_id)
                except ValueError:
                    print("❌ Please enter a valid task ID number")
            
            elif command == 'delete' and len(parts) > 1:
                try:
                    task_id = int(parts[1])
                    todo.delete_task(task_id)
                except ValueError:
                    print("❌ Please enter a valid task ID number")
            
            else:
                print("❌ Invalid command. Type 'help' for available commands.")
        
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break

if __name__ == "__main__":
    main()