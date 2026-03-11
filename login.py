import tkinter as tk
from tkinter import messagebox
import sqlite3
import subprocess
import sys

def login():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM admin WHERE username=? AND password=?", (name.get(), password.get()))
    user = c.fetchone()
    conn.close()

    if user:
        root.destroy()
        subprocess.Popen([sys.executable, "main.py"])
    else:
        messagebox.showerror("Thất bại", "Sai tài khoản hoặc mật khẩu!")

root = tk.Tk()
root.title("Đăng nhập")
root.geometry("400x400")

tk.Label(root, text="ĐĂNG NHẬP HỆ THỐNG", font=("Arial", 14, "bold")).pack(pady=30)

name = tk.StringVar()
password = tk.StringVar()

tk.Label(root, text="Tên đăng nhập:").pack()
tk.Entry(root, textvariable=name).pack(pady=5)
tk.Label(root, text="Mật khẩu:").pack()
tk.Entry(root, textvariable=password, show="*").pack(pady=5)

tk.Button(root, text="Đăng nhập", command=login, bg="#2ecc71", fg="white", width=15).pack(pady=20)

root.mainloop()