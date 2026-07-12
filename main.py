import tkinter as tk, json, customtkinter as ctk
import datetime
import random
from principles import *
from settings import *
from countdown import calculate_countdown

tasks = []
#principles
def rotate_principle():
    principle_label.configure(text=random.choice(principles))
    window.after(60000, rotate_principle)

countdown_labels = []   # parallel to tasks[]; index i = label for tasks[i]
task_frames = []         # parallel to tasks[]; index i = task_label_frame for tasks[i]
_update_countdowns_scheduled = False

def update_countdowns():
    global _update_countdowns_scheduled
    _update_countdowns_scheduled = True
    for task, label in zip(tasks, countdown_labels):
        try:
            label.configure(text=calculate_countdown(task))
        except tk.TclError:
            pass  # widget was destroyed between scheduling and running
    window.after(1000, update_countdowns)


#tasks
class Task:
    def __init__(self, text):
        self.text = text 
        self.completed = False 
        self.creation_date = datetime.datetime.now()

def load_tasks(filename="tasks.json"):
    with open(filename, "r") as file:
        tasks_data = json.load(file)
        tasks = []
        for task_data in tasks_data:
            task = Task(task_data['text'])
            task.completed = task_data.get('completed', False)
            task.creation_date = datetime.datetime.fromisoformat(task_data['creation_date'])
            tasks.append(task)

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
    if entry.get() != '':
        tasks.insert(0,Task(entry.get().strip()))  
        entry.delete(0, tk.END)  
        update_task_list()  
        save_tasks()

def complete_task(task):
    if task in tasks:
        task.completed = True
    reorder_tasks()
    update_task_list()
    save_tasks()

def reorder_tasks():
    tasks.sort(key=lambda t: t.completed)

def remove_task(task):
    if task in tasks:
        tasks.remove(task)
    update_task_list()
    save_tasks()

def update_task_list():
    for widget in task_list_frame.winfo_children():
        widget.destroy()
        countdown_labels.clear()

    for index, task in enumerate(tasks):
        task_label_frame = ctk.CTkFrame(task_list_frame,  fg_color= FG_COLOR)
        task_label_frame.pack(padx=5, pady=5, anchor='w', fill='x')

        #check button
        if not task.completed:
            check_button = ctk.CTkButton(task_label_frame,
            command=lambda i=task: complete_task(i), text = '',
            width=BUTTON_DIM, height=BUTTON_DIM,
            corner_radius=9, border_width=1, border_color= PRIMARY,
            fg_color = FG_COLOR,text_color=BLACK, hover_color=HOVER_COLOR)
            check_button.pack(padx=7, side = 'left')

        # delete button
        delete_button = ctk.CTkButton(task_label_frame,
            command=lambda i=task: remove_task(i), text = ' ✕ ', font=ctk.CTkFont(size=18),
            width=BUTTON_DIM, height=BUTTON_DIM,
            corner_radius=9, border_width=1, border_color= FG_COLOR,
            fg_color = FG_COLOR,text_color='red', hover_color=HOVER_COLOR)
        delete_button.pack(side='right', padx=(0, 7))

        #taks text
        task_label = ctk.CTkLabel(task_label_frame, 
                                  text=task.text, 
                                  font=ctk.CTkFont(size=14), 
                                  fg_color=FG_COLOR,
                                  text_color=WHITE,
                                  wraplength=240, 
                                  justify="left")
        if task.completed == True:
            task_label.configure(text_color= LIGHT_GRAY)
        task_label.pack(padx=5, pady=5, anchor='w') 



        # Add countdown display
        countdown_label = ctk.CTkLabel(task_label_frame,
                                        text=calculate_countdown(task),
                                        font=ctk.CTkFont(size=10), 
                                        fg_color=FG_COLOR,
                                        text_color='orange')
        if task.completed == True:
            countdown_label.configure(text_color=LIGHT_GRAY)
        countdown_label.pack(padx=5, pady=2, anchor='w')
        countdown_labels.append(countdown_label)
    save_tasks(filename="tasks.json") 
    update_countdowns()




# UI
window = ctk.CTk()
window.title("Cult of Done To-Do")
window.geometry('400x600')
window.minsize(400, 300)
window.resizable(True, True)
#window.iconbitmap('empty.ico') 
window.configure(fg_color=BLACK)

# main frame
frame = ctk.CTkFrame(window, corner_radius=0, fg_color= BLACK)
frame.pack(fill = 'x',side = 'top')


# entry
entry = ctk.CTkEntry(frame, placeholder_text="Add a task...", border_width=1 )
entry.pack(padx = 4, pady = 5, side = 'left', fill = 'both', expand = True)

# + button
font = ctk.CTkFont(weight ='bold', family = FONT, size = 23)
plus_button = ctk.CTkButton(frame,text = '+', command = add_task, font = font,
                            width=35, corner_radius=8, fg_color = PRIMARY, text_color=BLACK, hover_color=ACCENT, border_width=2, border_color= SECONDARY)
plus_button.pack(padx = 4, pady = 5, side = 'right', fill = 'x', expand = False)
window.bind('<Return>', lambda func: add_task())

# task list
task_list_frame = ctk.CTkScrollableFrame(window,scrollbar_button_color=FG_COLOR)
task_list_frame.pack(padx = 4, pady = 4, fill = 'both', anchor = 'n', expand = True)

# manifesto banner (sits below the task list)
principle_frame = ctk.CTkFrame(window, fg_color=BLACK)
principle_frame.pack(side='bottom', fill='x', padx=4, pady=4)
principle_label = ctk.CTkLabel(principle_frame, text="",
    font=ctk.CTkFont(size=11, slant="italic"),
    text_color=SECONDARY, wraplength=360, justify="center")
principle_label.pack(fill='x', padx=8, pady=6)

rotate_principle()

# run
window.mainloop()