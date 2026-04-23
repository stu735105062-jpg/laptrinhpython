from database import *

# Kết nối database
connect()

# Dữ liệu mẫu để insert
sample_tasks = [
    ("Học Python", "Hoàn thành bài tập về Tkinter", "25/04/2026", "14:00", "Chưa hoàn thành", 1),
    ("Đi mua sắm", "Mua thực phẩm cho tuần này", "24/04/2026", "10:00", "Chưa hoàn thành", 0),
    ("Gặp khách hàng", "Thảo luận về dự án mới", "26/04/2026", "15:30", "Chưa hoàn thành", 1),
    ("Tập thể dục", "Chạy bộ 30 phút", "23/04/2026", "07:00", "Hoàn thành", 0),
    ("Đọc sách", "Đọc cuốn sách về Machine Learning", "30/04/2026", "20:00", "Chưa hoàn thành", 1)
]

# Insert dữ liệu vào database
for task in sample_tasks:
    write(task)
    print(f"Đã thêm công việc: {task[0]}")

print("\nĐã insert thành công 5 công việc mẫu vào database!")