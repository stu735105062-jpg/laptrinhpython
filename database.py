import sqlite3
def login():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute(
        """
    SELECT * FROM admin;

"""
    )
def connect():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS congviec(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        task TEXT,
        deadline TEXT,
        status TEXT
    )
    """)

    conn.commit()
    conn.close()


def write(line):
    t = line.split('-')

    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    c.execute(
        "INSERT INTO congviec(task,deadline,status) VALUES(?,?,?)",
        (t[0], t[1], t[2])
    )

    conn.commit()
    conn.close()


def read():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    c.execute("SELECT task,deadline,status FROM congviec")
    data = c.fetchall()

    conn.close()

    cv = []
    for i in data:
        cv.append(list(i))

    return cv


def delete(index):
    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    c.execute("SELECT id FROM congviec")
    data = c.fetchall()

    if index < len(data):
        id = data[index][0]
        c.execute("DELETE FROM congviec WHERE id=?", (id,))

    conn.commit()
    conn.close()


def update(index, line):
    t = line.split('-')

    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    c.execute("SELECT id FROM congviec")
    data = c.fetchall()

    if index < len(data):
        id = data[index][0]

        c.execute("""
        UPDATE congviec
        SET task=?, deadline=?, status=?
        WHERE id=?
        """, (t[0], t[1], t[2], id))

    conn.commit()
    conn.close()