import json
import datetime
from main import Task

tasks = []

def load_tasks(filename="tasks.json"):
    with open(filename, "r") as file:
        tasks_data = json.load(file)
        
        for task_data in tasks_data:
            task = Task(task_data['text'])
            task.completed = task_data.get('completed', False)
            task.creation_date = datetime.datetime.fromisoformat(task_data['creation_date'])
            tasks.append(task)
    return tasks

def save_tasks(filename="tasks.json"):
    with open(filename, "w") as file:
        tasks_to_save = []
        for task in tasks:
            task_dict = {
                'text': task.text,
                'completed': task.completed,
                'creation_date': task.creation_date.isoformat()
            }
            tasks_to_save.append(task_dict)
        json.dump(tasks_to_save, file, indent=4)

def add_task():
    tasks.insert(0,Task(entry.get().strip()))  
    update_task_list()  
    save_tasks()

def complete_task(task):
    if task in tasks:
        task.completed = True
    tasks.sort(key=lambda t: t.completed)
    update_task_list()
    return True


def remove_task(task):
    if task in tasks:
        tasks.remove(task)
        update_task_list()
    return True