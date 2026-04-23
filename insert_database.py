import sqlite3

def insert_multiple_tasks():
    """Insert nhiều công việc cùng lúc vào database"""

    # Kết nối database
    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    # Dữ liệu mẫu để insert
    tasks_to_insert = [
        ("Họp nhóm", "Thảo luận tiến độ dự án", "27/04/2026", "09:00", "Chưa hoàn thành", 1),
        ("Viết báo cáo", "Báo cáo tháng 4", "28/04/2026", "16:00", "Chưa hoàn thành", 1),
        ("Đi gym", "Tập luyện sức khỏe", "24/04/2026", "18:00", "Chưa hoàn thành", 0),
        ("Gọi điện", "Liên hệ khách hàng VIP", "25/04/2026", "11:00", "Chưa hoàn thành", 1),
        ("Mua quà", "Quà sinh nhật bạn bè", "29/04/2026", "14:00", "Chưa hoàn thành", 0),
        ("Sửa máy tính", "Fix lỗi phần mềm", "26/04/2026", "13:00", "Chưa hoàn thành", 1),
        ("Đọc tài liệu", "Nghiên cứu công nghệ mới", "01/05/2026", "19:00", "Chưa hoàn thành", 0),
        ("Nấu ăn", "Chuẩn bị bữa tối gia đình", "23/04/2026", "17:30", "Hoàn thành", 0),
    ]

    # Insert từng task
    inserted_count = 0
    for task in tasks_to_insert:
        try:
            c.execute("""
                INSERT INTO congviec(work, des, deadline_date, deadline_time, status, important)
                VALUES(?,?,?,?,?,?)
            """, task)
            inserted_count += 1
            print(f"✅ Đã thêm: {task[0]}")
        except Exception as e:
            print(f"❌ Lỗi khi thêm '{task[0]}': {e}")

    # Commit và đóng kết nối
    conn.commit()
    conn.close()

    print(f"\n🎉 Đã insert thành công {inserted_count}/{len(tasks_to_insert)} công việc!")

def insert_custom_task(work, des, deadline_date, deadline_time, status="Chưa hoàn thành", important=0):
    """Insert một công việc tùy chỉnh"""
    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    try:
        c.execute("""
            INSERT INTO congviec(work, des, deadline_date, deadline_time, status, important)
            VALUES(?,?,?,?,?,?)
        """, (work, des, deadline_date, deadline_time, status, important))

        conn.commit()
        print(f"✅ Đã thêm công việc: {work}")
    except Exception as e:
        print(f"❌ Lỗi: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    print("Chọn cách insert:")
    print("1. Insert nhiều công việc mẫu")
    print("2. Insert công việc tùy chỉnh")

    choice = input("Nhập lựa chọn (1/2): ").strip()

    if choice == "1":
        insert_multiple_tasks()
    elif choice == "2":
        work = input("Tên công việc: ").strip()
        des = input("Mô tả: ").strip()
        date = input("Ngày deadline (dd/mm/yyyy): ").strip()
        time_input = input("Giờ deadline (hh:mm): ").strip()
        important = 1 if input("Quan trọng? (y/n): ").strip().lower() in ['y', 'yes', '1'] else 0

        insert_custom_task(work, des, date, time_input, "Chưa hoàn thành", important)
    else:
        print("Lựa chọn không hợp lệ!")