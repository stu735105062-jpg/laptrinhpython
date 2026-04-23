from database import *

def add_task():
    print("=== THÊM CÔNG VIỆC MỚI ===")

    # Nhập thông tin công việc
    work = input("Tên công việc: ").strip()
    if not work:
        print("Tên công việc không được để trống!")
        return

    des = input("Mô tả: ").strip()
    deadline_date = input("Ngày deadline (dd/mm/yyyy): ").strip()
    deadline_time = input("Giờ deadline (hh:mm): ").strip()
    status = "Chưa hoàn thành"  # Mặc định

    # Quan trọng
    important_input = input("Quan trọng? (y/n): ").strip().lower()
    important = 1 if important_input in ['y', 'yes', 'có', '1'] else 0

    # Tạo tuple dữ liệu
    task_data = (work, des, deadline_date, deadline_time, status, important)

    # Insert vào database
    try:
        write(task_data)
        print(f"\n✅ Đã thêm công việc '{work}' thành công!")
    except Exception as e:
        print(f"\n❌ Lỗi khi thêm công việc: {e}")

if __name__ == "__main__":
    connect()  # Kết nối database
    add_task()