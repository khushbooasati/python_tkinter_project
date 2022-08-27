
from tkinter import *
from time import strftime
from xmlrpc.client import _strftime

root = Tk()
root.title("digital computer clock")

def time():
    string = _strftime("%H:%M:%S:%P")
    lbl.config(text = string)
    lbl.after(1000, time)


lbl = Label(root,font="aerial", 160, "bold",bg="black",fg="white")  
lbl.pack(anchor='center',fill="both",expand=1)  
