import tkinter as tk, json, customtkinter as ctk; from tkinter import ttk; from settings import *


tasks = []
class Task:
    def __init__(self, text):
        self.text = text 
        self.completed = False 

#def load_tasks(filename="tasks.json"):
#    with open(filename, "w") as file:
#        tasks = json.loads(tasks.json)

def save_tasks(filename="tasks.json"):
    with open(filename, "w") as file:
        json.dump([task.text for task in tasks], file, indent=4)

def add_task():
    if entry.get() != '':
        tasks.insert(0,Task(entry.get().strip()))  
        entry.delete(0, tk.END)  
        update_task_list()  

def remove_task(index):
    del tasks[index]  
    update_task_list()

def update_task_list():
#   load_tasks(filename="tasks.json")
    for widget in task_list_frame.winfo_children():
        widget.destroy()

    for index, task in enumerate(tasks):
        task_label_frame = ctk.CTkFrame(task_list_frame,  fg_color='#343638')
        task_label_frame.pack(padx=5, pady=5, anchor='w', fill='x')

        check_button = ctk.CTkButton(task_label_frame,
            command=lambda i=index: remove_task(i), text = '',
            width=CHECK_BUTTON_DIM, height=CHECK_BUTTON_DIM,
            corner_radius=9, border_width=1, border_color= PRIMARY,
            fg_color = "#343638",text_color=BLACK, hover_color='#2b2b2b')
        check_button.pack(padx=7, side = 'left')

        task_label = ctk.CTkLabel(task_label_frame, text=task.text, font=ctk.CTkFont(size=14), fg_color='#343638',text_color='white', corner_radius = 5)
        task_label.pack(padx=5, pady=5, anchor='w') 
    save_tasks(filename="tasks.json") 


# window
window = ctk.CTk()
window.title("")
window.geometry('400x600')
#window.iconbitmap('empty.ico') 
window.configure(fg_color=BLACK)

# main frame
frame = ctk.CTkFrame(window, corner_radius=0, fg_color= BLACK)
frame.pack(fill = 'x',side = 'top')

# task list
task_list_frame = ctk.CTkFrame(window)
task_list_frame.pack(padx = 4, pady = 4, fill = 'both', anchor = 'n', expand = True)

# entry
entry = ctk.CTkEntry(frame, placeholder_text="Add a task", border_width=1 )
entry.pack(padx = 4, pady = 5, side = 'left', fill = 'both', expand = True)

# + button
font = ctk.CTkFont(weight ='bold', family = FONT, size = 23)
plus_button = ctk.CTkButton(frame,text = '+', command = add_task, font = font,
                            width=35, corner_radius=8, fg_color = PRIMARY, text_color=DARK_TEXT, hover_color=ACCENT, border_width=2, border_color= SECONDARY)
plus_button.pack(padx = 4, pady = 5, side = 'right', fill = 'x', expand = False)
window.bind('<Return>', lambda func: add_task())
# run
window.mainloop()