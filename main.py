import tkinter as tk
from tkinter import ttk
import customtkinter as ctk

from settings import *

#window
window = ctk.CTk()
window.title("")
window.geometry('400x600')
window.iconbitmap('empty.ico') 
window.configure(fg_color='#202020')

#main frame
frame = ctk.CTkFrame(window, corner_radius=0, fg_color= '#202020')
frame.pack(fill = 'x',side = 'top')

#task list
task_list_frame = ctk.CTkFrame(window)
task_list_frame.pack(padx = 4, pady = 4, fill = 'both', anchor = 'n', expand = True)


#entry
entry = ctk.CTkEntry(frame, placeholder_text="Add a task", border_width=1 )
entry.pack(padx = 4, pady = 5, side = 'left', fill = 'both', expand = True)

# + button
font = ctk.CTkFont(weight ='bold', family = FONT, size = 23)
plus_button = ctk.CTkButton(frame ,text = '+', font = font, width=35, corner_radius=8, fg_color = GREEN,text_color=BLACK, hover_color=DARK_GREEN, border_width=2, border_color= DARK_GREEN)
plus_button.pack(padx = 4, pady = 5, side = 'right', fill = 'x', expand = False)





#run
window.mainloop()