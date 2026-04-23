import os
import sqlite3

DB_PATH = os.path.join(os.path.dirname(__file__), "database.db")

def connect():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS congviec(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        work TEXT, des TEXT, deadline_date TEXT, deadline_time TEXT, status TEXT, important BOOLEAN DEFAULT "False")""")
    conn.commit()
    conn.close()

def write(task_data):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO congviec(work, des, deadline_date, deadline_time, status, important) VALUES(?,?,?,?,?,?)", task_data)
    conn.commit()
    conn.close()

def read():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT work, des, deadline_date, deadline_time, status, important FROM congviec")
    data = c.fetchall()
    conn.close()
    return [list(i) for i in data]

def delete(id_xoa):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM congviec WHERE id=?", (id_xoa,))
    conn.commit()
    conn.close()

def update(id_sua, work, des, date, time, status, important):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("UPDATE congviec SET work=?, des=?, deadline_date=?, deadline_time=?, status=?, important=? WHERE id=?", 
                  (work, des, date, time, status, important, id_sua))
    conn.commit()
    conn.close()

def get_work_by_id(id_work):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id, work, des, deadline_date, deadline_time, status, important FROM congviec WHERE id=?", (id_work,))
    data = c.fetchone()
    conn.close()
    return data

def get_work_by_date(date):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id, work, des, deadline_date, deadline_time, status, important FROM congviec WHERE deadline_date=? ORDER BY deadline_time ASC", (date,))
    data = c.fetchall()
    conn.close()
    return [list(i) for i in data]