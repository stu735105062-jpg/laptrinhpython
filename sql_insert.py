import sqlite3

def insert_with_sql():
    """Insert dữ liệu sử dụng câu lệnh SQL trực tiếp"""

    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    # Ví dụ các câu lệnh INSERT SQL
    sql_commands = [
        """
        INSERT INTO congviec(work, des, deadline_date, deadline_time, status, important)
        VALUES('Làm bài tập', 'Hoàn thành bài tập Toán', '24/04/2026', '20:00', 'Chưa hoàn thành', 0)
        """,

        """
        INSERT INTO congviec(work, des, deadline_date, deadline_time, status, important)
        VALUES('Đi chơi', 'Đi công viên với bạn bè', '25/04/2026', '15:00', 'Chưa hoàn thành', 0)
        """,

        """
        INSERT INTO congviec(work, des, deadline_date, deadline_time, status, important)
        VALUES('Học tiếng Anh', 'Ôn tập từ vựng mới', '26/04/2026', '19:00', 'Chưa hoàn thành', 1)
        """
    ]

    inserted_count = 0
    for sql in sql_commands:
        try:
            c.execute(sql)
            inserted_count += 1
            print(f"✅ Đã thực thi câu SQL {inserted_count}")
        except Exception as e:
            print(f"❌ Lỗi SQL: {e}")

    conn.commit()
    conn.close()

    print(f"\n🎉 Đã insert thành công {inserted_count} công việc bằng SQL!")

def custom_sql_insert(sql_command):
    """Thực thi câu lệnh INSERT SQL tùy chỉnh"""
    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    try:
        c.execute(sql_command)
        conn.commit()
        print("✅ Đã thực thi câu SQL thành công!")
    except Exception as e:
        print(f"❌ Lỗi SQL: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    print("=== INSERT DỮ LIỆU VÀO DATABASE ===")
    print("1. Insert dữ liệu mẫu bằng SQL")
    print("2. Thực thi câu SQL tùy chỉnh")
    print("3. Xem hướng dẫn SQL")

    choice = input("Chọn (1/2/3): ").strip()

    if choice == "1":
        insert_with_sql()
    elif choice == "2":
        print("\nNhập câu lệnh INSERT SQL (ví dụ):")
        print("INSERT INTO congviec(work, des, deadline_date, deadline_time, status, important) VALUES('Tên', 'Mô tả', 'dd/mm/yyyy', 'hh:mm', 'Chưa hoàn thành', 0)")
        sql = input("\nCâu SQL: ").strip()
        if sql:
            custom_sql_insert(sql)
    elif choice == "3":
        print("\n=== HƯỚNG DẪN INSERT DỮ LIỆU ===")
        print("Cấu trúc bảng congviec:")
        print("- id: INTEGER PRIMARY KEY AUTOINCREMENT (tự động)")
        print("- work: TEXT (tên công việc)")
        print("- des: TEXT (mô tả)")
        print("- deadline_date: TEXT (ngày dd/mm/yyyy)")
        print("- deadline_time: TEXT (giờ hh:mm)")
        print("- status: TEXT (Chưa hoàn thành/Hoàn thành)")
        print("- important: BOOLEAN (0 = Không, 1 = Có)")
        print()
        print("Ví dụ câu INSERT:")
        print("INSERT INTO congviec(work, des, deadline_date, deadline_time, status, important)")
        print("VALUES('Tên công việc', 'Mô tả chi tiết', '25/04/2026', '14:30', 'Chưa hoàn thành', 1);")
    else:
        print("Lựa chọn không hợp lệ!")