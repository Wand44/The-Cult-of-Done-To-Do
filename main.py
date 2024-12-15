import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from ctypes import windll, byref, sizeof, c_int

from settings import *

tasks = []

    
def add_task():
    task_text = entry.get()
    if task_text.strip():  # Don't add empty tasks
        tasks.append(task_text)  # Add task to the list
        entry.delete(0, tk.END)  # Clear the entry widget
        update_task_list()  # Update the task display

def remove_task(index):
    del tasks[index]  # Remove task from the list
    update_task_list()

# update the displayed tasks
def update_task_list():
    # Clear the existing tasks from the task list frame
    for widget in task_list_frame.winfo_children():
        widget.destroy()
    # Create a new label for each task in the task list
    for index, task in enumerate(tasks):
        task_label_frame = ctk.CTkFrame(task_list_frame,  fg_color='#343638')
        task_label_frame.pack(padx=5, pady=5, anchor='w', fill='x')

        check_button = ctk.CTkButton(task_label_frame, command=lambda i=index: remove_task(i), text = '',
                                    width=CHECK_BUTTON_DIM, height=CHECK_BUTTON_DIM, corner_radius=9, border_width=1, border_color= PRIMARY,
                                    fg_color = "#343638",text_color=BLACK, hover_color='#2b2b2b')
        check_button.pack(padx=7, side = 'left')

        task_label = ctk.CTkLabel(task_label_frame, text=task, font=ctk.CTkFont(size=14), fg_color='#343638',text_color='white', corner_radius = 5)
        task_label.pack(padx=5, pady=5, anchor='w')


# window
window = ctk.CTk()
window.title("")
window.geometry('400x600')
window.iconbitmap('empty.ico') 
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