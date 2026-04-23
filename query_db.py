import sqlite3

conn = sqlite3.connect('database.db')
c = conn.cursor()
c.execute("SELECT id, work, des, deadline_date, deadline_time, status, important FROM congviec WHERE deadline_date='23/04/2026'")
rows = c.fetchall()
print('count', len(rows))
for row in rows:
    print(row)
conn.close()
