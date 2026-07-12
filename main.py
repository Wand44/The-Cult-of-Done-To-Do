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
    for task, label in zip(tasks, countdown_labels):
        try:
            label.configure(text=calculate_countdown(task))
        except tk.TclError:
            pass
    window.after(1000, update_countdowns)

def start_countdown_loop():
    global _update_countdowns_scheduled
    if not _update_countdowns_scheduled:
        _update_countdowns_scheduled = True
        update_countdowns()

#tasks
class Task:
    def __init__(self, text):
        self.text = text
        self.completed = False
        self.creation_date = datetime.datetime.now()

    def complete(self):
        self.completed = True

    def to_dict(self):
        return {
            'text': self.text,
            'completed': self.completed,
            'creation_date': self.creation_date.isoformat()
        }

    @classmethod
    def from_dict(cls, data):
        task = cls(data['text'])
        task.completed = data.get('completed', False)
        task.creation_date = datetime.datetime.fromisoformat(data['creation_date'])
        return task

def load_tasks(filename="tasks.json"):
    try:
        with open(filename, "r", encoding="utf-8") as file:
            tasks_data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []
    return [Task.from_dict(td) for td in tasks_data]


def save_tasks(filename="tasks.json"):
    with open(filename, "w") as file:
        json.dump([task.to_dict() for task in tasks], file, indent=4)


def complete_task(task):
    if task in tasks and not task.completed:
        idx = tasks.index(task)
        task.completed = True

        frame = task_frames.pop(idx)
        clabel = countdown_labels.pop(idx)
        tasks.pop(idx)

        # first index that's already completed = where this task should land
        insert_idx = next((i for i, t in enumerate(tasks) if t.completed), len(tasks))
        tasks.insert(insert_idx, task)
        task_frames.insert(insert_idx, frame)
        countdown_labels.insert(insert_idx, clabel)

        reposition_frame(insert_idx)
        apply_completed_style(frame)
        save_tasks()


def reposition_frame(idx):
    frame = task_frames[idx]
    if idx > 0:
        frame.pack(after=task_frames[idx - 1])
    elif len(task_frames) > 1:
        frame.pack(before=task_frames[1])


def add_task():
    if entry.get() != '':
        new_task = Task(entry.get().strip())
        tasks.insert(0, new_task)
        entry.delete(0, tk.END)

        before = task_frames[0] if task_frames else None
        frame, clabel = create_task_row(new_task, before=before)
        task_frames.insert(0, frame)
        countdown_labels.insert(0, clabel)

        save_tasks()


def remove_task(task):
    if task in tasks:
        idx = tasks.index(task)
        task_frames[idx].destroy()
        tasks.pop(idx)
        task_frames.pop(idx)
        countdown_labels.pop(idx)
        save_tasks()

def create_task_row(task, before=None):
    task_label_frame = ctk.CTkFrame(task_list_frame, fg_color=FG_COLOR, corner_radius=8)
    if before is not None:
        task_label_frame.pack(padx=0, pady=0, anchor='w', fill='x', before=before)
    else:
        task_label_frame.pack(padx=0, pady=0, anchor='w', fill='x')
    # check button
    check_button = ctk.CTkButton(task_label_frame, command=lambda: complete_task(task), text='',
        width=BUTTON_DIM, height=BUTTON_DIM, corner_radius=9, border_width=2,
        border_color=PRIMARY, fg_color=FG_COLOR, hover_color=HOVER_COLOR)
    check_button.pack(padx=(10, 4), side='left')
    # delete button
    delete_button = ctk.CTkButton(task_label_frame, command=lambda: remove_task(task), text=' ✕ ',
        width=BUTTON_DIM, height=BUTTON_DIM, corner_radius=9, border_width=1,
        border_color=FG_COLOR, fg_color=FG_COLOR, text_color='red', hover_color=FG_COLOR)
    delete_button.pack(side='right', padx=2)
    #task text
    task_label = ctk.CTkLabel(task_label_frame, text=task.text, font=ctk.CTkFont(size=14),
        fg_color=FG_COLOR, text_color=WHITE, wraplength=240, justify="left")
    task_label.pack(padx=5, pady=1, anchor='w')
    # countdown
    countdown_label = ctk.CTkLabel(task_label_frame, text=calculate_countdown(task),
        font=ctk.CTkFont(size=10), fg_color=FG_COLOR, text_color='orange')
    countdown_label.pack(padx=5, pady=2, anchor='w')

    # stash refs on the frame so complete_task can restyle this row later
    task_label_frame.check_button = check_button
    task_label_frame.task_label = task_label
    task_label_frame.countdown_label = countdown_label

    if task.completed:
        apply_completed_style(task_label_frame)
    return task_label_frame, countdown_label

def apply_completed_style(frame):
    frame.check_button.configure(border_color=LIGHT_GRAY, fg_color=LIGHT_GRAY, hover_color=LIGHT_GRAY)
    frame.task_label.configure(text_color=LIGHT_GRAY, font=ctk.CTkFont(overstrike=True))
    frame.countdown_label.configure(text_color=LIGHT_GRAY, font=ctk.CTkFont(size=10))

def build_initial_task_list():
    countdown_labels.clear()
    task_frames.clear()
    for task in tasks:
        frame, clabel = create_task_row(task)
        task_frames.append(frame)
        countdown_labels.append(clabel)





# UI
window = ctk.CTk()
window.title("")
window.geometry('400x600')
window.minsize(400, 300)
window.resizable(True, True)
window.iconbitmap('empty.ico') 
window.configure(fg_color=BLACK)


# main frame
frame = ctk.CTkFrame(window, corner_radius=0, fg_color= BLACK)
frame.pack(fill = 'x',side = 'top')

# entry
entry = ctk.CTkEntry(frame, placeholder_text="Add a task...", border_width=1 )
entry.pack(padx = 4, pady = 5, side = 'left', fill = 'both', expand = True)
tasks = load_tasks()

# + button
font = ctk.CTkFont(weight ='bold', family = FONT, size = 18)
plus_button = ctk.CTkButton(frame,text = '+', command = add_task, font = font,
                            width=35, 
                            corner_radius=8, 
                            fg_color = PRIMARY, 
                            text_color=BLACK, 
                            hover_color=ACCENT, 
                            border_width=2, 
                            border_color= SECONDARY)
plus_button.pack(padx = 4, pady = 5, side = 'right', fill = 'x')
window.bind('<Return>', lambda func: add_task())

# task list
task_list_frame = ctk.CTkScrollableFrame(window,scrollbar_button_color=FG_COLOR,corner_radius=12)
task_list_frame.pack(padx = 5, pady = 5, fill = 'both', anchor = 'n', expand = True)

build_initial_task_list()
start_countdown_loop()
# manifesto banner (sits below the task list)
principle_frame = ctk.CTkFrame(window, fg_color=BLACK)
principle_frame.pack(side='bottom', fill='x', padx=0, pady=0)
principle_label = ctk.CTkLabel(principle_frame, text="",
    font=ctk.CTkFont(size=12, slant="italic",weight="bold"),
    text_color=SECONDARY, wraplength=380, justify="center")
principle_label.pack(fill='both', padx=0, pady=10)
rotate_principle()
window.mainloop()