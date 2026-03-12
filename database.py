import sqlite3

def connect():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS congviec(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        work TEXT, des TEXT, deadline_date TEXT, deadline_time TEXT, status TEXT, important BOOLEAN DEFAULT "False")""")
    c.execute("""CREATE TABLE IF NOT EXISTS admin(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL, password TEXT NOT NULL)""")
    c.execute("SELECT COUNT(*) FROM admin")
    if c.fetchone()[0] == 0:
        c.execute("INSERT INTO admin (username, password) VALUES ('admin', '123')")
    conn.commit()
    conn.close()

def write(task_data):
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("INSERT INTO congviec(work, des, deadline_date, deadline_time, status, important) VALUES(?,?,?,?,?,?)", task_data)
    conn.commit()
    conn.close()

def read():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("SELECT work, des, deadline_date, deadline_time, status, important FROM congviec")
    data = c.fetchall()
    conn.close()
    return [list(i) for i in data]

def get_ids():
    """Hàm phụ để lấy danh sách ID, phục vụ cho việc xóa/sửa"""
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("SELECT id FROM congviec")
    ids = [row[0] for row in c.fetchall()]
    conn.close()
    return ids

def delete(id_xoa):
    ids = get_ids()
    if index < len(ids):
        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute("DELETE FROM congviec WHERE id=?", (id_xoa,))
        conn.commit()
        conn.close()

def update(id_sua, work, des, date, time, status, important):
    ids = get_ids()
    if index < len(ids):
        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute("UPDATE congviec SET work=?, des=?, deadline_date=?, deadline_time=?, status=?, important=? WHERE id=?", 
                  (work, des, date, time, status, important, id_sua))
        conn.commit()
        
        conn.close()

def get_work_by_date(date):
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("SELECT id, work, des, deadline_date, deadline_time, status, important FROM congviec WHERE deadline_date=? ORDER BY deadline_time ASC", (date,))
    data = c.fetchall()
    conn.close()
    return [list(i) for i in data]
