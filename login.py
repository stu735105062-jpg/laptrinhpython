import tkinter
from tkinter import ttk
import sqlite3
import os

def login():
    conn=sqlite3.connect('database.db')
    c=conn.cursor()
    c.execute(
        """
    SELECT * FROM admin;
"""
    )
    mk=[]
    ds=c.fetchall()
    for i in ds:
        mk.append(list(i))
    for i in mk:
        if i[1]==name.get() and i[2]==password.get():
           os.system("Python main.py")
        else:
            tkinter.Label(frame,text="Sai mật khẩu hoặc tên đăng nhập").pack()


root = tkinter.Tk()
root.title("Hệ thống đăng nhập")
root.geometry("500x500")
root.resizable(False, False)   # không cho resize
tkinter.Label(root, text="Hệ thống đăng nhập quản lý công việc",
              font=("Arial", 16)).pack(pady=20)
frame = tkinter.Frame(root)
frame.pack(pady=50)

name = tkinter.StringVar()
password = tkinter.StringVar()



tkinter.Label(frame, text="Tên đăng nhập:").pack(pady=5)
tkinter.Entry(frame, textvariable=name, width=40).pack(pady=5)

tkinter.Label(frame, text="Mật khẩu:").pack(pady=5)
tkinter.Entry(frame, textvariable=password, show="*", width=40).pack(pady=5)

tkinter.Button(frame, text="Đăng nhập", width=20,command=login).pack(pady=20)

root.mainloop()