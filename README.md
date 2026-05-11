# Quản Lý Công Việc Chuyên Nghiệp

Đây là một ứng dụng quản lý công việc được viết bằng Python, sử dụng giao diện đồ họa Tkinter với thư viện ttkbootstrap để tạo giao diện hiện đại. Ứng dụng cho phép người dùng thêm, xem, cập nhật và xóa các công việc với deadline, thời gian, và mức độ quan trọng.

## Tính Năng Chính

- **Thêm công việc mới**: Sử dụng form nhập liệu với tên công việc, mô tả, deadline, thời gian, và đánh dấu quan trọng.
- **Hiển thị danh sách công việc**: Lọc theo trạng thái (Tất cả, Hoàn thành, Chưa hoàn thành).
- **Thông báo**: Tự động thông báo khi đến giờ làm việc.
- **Lịch**: Chọn ngày deadline bằng calendar picker.
- **Cơ sở dữ liệu**: Lưu trữ dữ liệu trong SQLite.

## Cấu Trúc Dự Án

Dự án bao gồm các file Python sau:

- `main.py`: File chính, chứa giao diện chính và logic ứng dụng.
- `database.py`: Xử lý cơ sở dữ liệu SQLite.
- `add_work.py`: Form thêm công việc mới.
- `calender.py`: Dialog chọn ngày.
- `test.py`: File test (có thể là ví dụ đọc file).

## Yêu Cầu Hệ Thống

- Python 3.x
- Thư viện: tkinter, ttkbootstrap, windows_toasts

## Cài Đặt và Chạy

1. Cài đặt các thư viện cần thiết:
   ```
   pip install ttkbootstrap windows-toasts
   ```

2. Chạy ứng dụng:
   ```
   python main.py
   ```

## Sơ Đồ UML

Xem sơ đồ UML chi tiết tại [diagram.puml](diagram.puml).

Để xem sơ đồ, bạn có thể sao chép mã PlantUML từ file trên vào công cụ trực tuyến như [PlantUML Online](https://www.plantuml.com/plantuml/uml/) hoặc sử dụng extension VS Code để render.

## Phát Triển

- Giao diện sử dụng ttkbootstrap để có theme đẹp.
- Cơ sở dữ liệu SQLite đơn giản.
- Thông báo sử dụng windows_toasts cho Windows.

## Tác Giả

[Nguyễn Bấ Lương, Nguyễn Trung Sơn]

## Giấy Phép

MIT License
