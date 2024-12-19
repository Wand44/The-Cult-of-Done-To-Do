import tkinter as tk, json, customtkinter as ctk; from tkinter import ttk; from settings import *


window = ctk.CTk()
window.title("")
window.geometry('400x600')
#window.iconbitmap('empty.ico') 
window.configure(fg_color='black')


a = ctk.CTkSegmentedButton(window, values=[".", "'", ","], text_color='gray', fg_color='gray', bg_color='gray',unselected_color = 'gray' ,  corner_radius= 50, width= 1, height= 1) 
a.pack() 

window.mainloop()