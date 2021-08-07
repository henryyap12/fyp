import tkinter as tk
from tkinter import filedialog, Text
import pandas as pd
from tkinter import *
from PIL import ImageTk, Image
from detect import detect
import cv2
from omr import omrmarking
import os

def getCSV():
    import_file_path = filedialog.askopenfilename()
    global csvpath
    csvpath = import_file_path
    return import_file_path


def build():
    window = Tk()
    window.title('Automatic OMR Grading System')
    window.iconbitmap('logo.ico')
    window.geometry("800x800")
    window.maxsize(height=920, width=900)
    window.minsize(height=920, width=900)
    window.config(background="white")
    return window


def show(p):
    img = Image.open(p)
    img = img.resize((550, 750))
    img = ImageTk.PhotoImage(img)
    panel = Label(window, image=img)
    panel.image = img
    panel.place(x=315, y=140)


def openfile():
    filename = filedialog.askopenfilename(title='open')
    global path
    path = filename
    return filename


def openImg():
    x = openfile()
    show(x)


def getTextInput():
    marks = totalmark.get(1.0, tk.END + "-1c")
    choice = totalchoice.get(1.0, tk.END + "-1c")
    c,s = omrmarking(path, csvpath, marks, choice)
    s = round(s,3)
    correct = Label(window, bg="#d3d3d3", text=c, fg='green', font=('arial', 14, 'bold'))
    correct.place(x=165, y=620, width=50)
    result = Label(window, bg="#d3d3d3", text=s, fg='green', font=('arial', 14, 'bold'))
    result.place(x=150, y=580, width=50)


window = build()
label = Label(window, text=" ", font=('arial', 22, 'bold'), width=15, height=100,bg="#d3d3d3")
label.place(x=0, y=0)
label_file_explorer = Label(window, text="Automatic OMR Grading ", font=('arial', 20, 'bold'), width=60, height=4,bg="#4ABDAC", fg="white")
label_file_explorer.place(x=-60, y=0)
label_file_explorer.option_add('*Font', 'Times 10')

button_explore = tk.Button(window, text="Browse Omr Sheet", command=openImg)
button_explore.place(x=50, y=170, width=180, height=40)

browseButton_CSV = tk.Button(window, text="Import CSV File", command=getCSV)
browseButton_CSV.place(x=50, y=250, width=180, height=40)

btnRead = tk.Button(window, height=1, width=10, text="Scan", command=getTextInput)
btnRead.place(x=50, y=700, width=180, height=40)

labelmark = Label(window, bg="#d3d3d3", text="Insert Total mark").place(x=50, y=320)
totalmark = tk.Text(window, height=30)
totalmark.place(x=50, y=345, width=120, height=20)

labelchoice = Label(window, bg="#d3d3d3", text="Insert Total choice").place(x=50, y=380)
totalchoice = tk.Text(window, height=30)
totalchoice.place(x=50, y=405, width=120, height=20)

resultlabel = Label(window, bg="#d3d3d3", text="Result:", font=('arial', 14, 'bold')).place(x=50, y=580)
correctlabel = Label(window, bg="#d3d3d3", text="Correct:", font=('arial', 14, 'bold')).place(x=50, y=620)

window.mainloop()
