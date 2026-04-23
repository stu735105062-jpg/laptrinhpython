from database import *
import sqlite3

# Kết nối và đọc dữ liệu
connect()

print("Dữ liệu trong database:")
print("-" * 100)
print(f"{'ID':<3} {'Công việc':<15} {'Mô tả':<30} {'Ngày':<12} {'Giờ':<8} {'Trạng thái':<15} {'Quan trọng':<10}")
print("-" * 100)

# Lấy dữ liệu với ID
conn = sqlite3.connect("database.db")
c = conn.cursor()
c.execute("SELECT id, work, des, deadline_date, deadline_time, status, important FROM congviec")
all_data = c.fetchall()
conn.close()

for row in all_data:
    id_val, work, des, date, time_val, status, important = row
    imp_text = "Có" if important else "Không"
    # Cắt ngắn mô tả nếu quá dài
    des_short = des[:27] + "..." if len(des) > 27 else des
    work_short = work[:14] + "..." if len(work) > 14 else work
    print(f"{id_val:<3} {work_short:<15} {des_short:<30} {date:<12} {time_val:<8} {status:<15} {imp_text:<10}")

print(f"\nTổng cộng: {len(all_data)} công việc")