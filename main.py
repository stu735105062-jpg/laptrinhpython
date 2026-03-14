from database import *
from tkinter import *
from tkinter import ttk, messagebox
import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
from add_work import DataEntryForm
from calender import DatePickerDialog
import datetime 
import time

connect()
root = ttkb.Window(themename="superhero")

sc_width = root.winfo_screenwidth()
sc_hight = root.winfo_screenheight()

hight_app_default = 500
width_app_default = 800

width_app_now = root.winfo_width()
hight_app_now = root.winfo_height()

center_x = (sc_width//2 - width_app_default // 2)
center_y = (sc_hight//2 - hight_app_default // 2)

root.resizable(False,False)

root.title("Quản lý công việc chuyên nghiệp")
root.geometry(f'{width_app_default}x{hight_app_default}+{center_x}+{center_y}')

selected_id = None

now = time.localtime()
year,month,day,*_= now
make_time = datetime.date(year=year,month=month,day=day)

time_make = make_time.strftime("%d/%m/%Y")


# --- CÁC HÀM XỬ LÝ DỮ LIỆU ---

def open_calendar():
    global time_make
    dialog = DatePickerDialog(title="Chọn ngày")
    if dialog.date_selected:
        time_make = dialog.date_selected.strftime('%d/%m/%Y')
        date_label.config(text=time_make)
        show(loc_box.get())
        return time_make

def show(filter_val="Tất cả"):
    for i in tree.get_children():
        tree.delete(i)

    data = get_work_by_date(time_make)
    today = datetime.date.today()

    for row in data:
        db_id, work, des, deadline_date, deadline_time, status, important = row

        if filter_val == "Tất cả" or status == filter_val:
            is_expired = False
            if status == "Chưa hoàn thành":
                try:
                    deadline = datetime.datetime.strptime(deadline_date, '%d/%m/%Y').date()
                    if deadline < today:
                        is_expired = True
                except Exception:
                    pass

            imp_text = 'Có' if str(important).lower() in ('1', 'true') else 'Không'

            iid = tree.insert('', END, iid=db_id, values=(work, deadline_time, status, imp_text))
            if is_expired:
                tree.item(iid, tags=('expired',))

    tree.tag_configure('expired', foreground='#FF5555', font=('Arial', 10, 'bold'))

def loc_du_lieu(event):
    show(loc_box.get())

def check_alerts():
    today = datetime.date.today()
    expired_tasks = []
    for row in read():
        status = row[4]
        if status == "Chưa hoàn thành":
            try:
                deadline = datetime.datetime.strptime(row[2], '%d/%m/%Y').date()
                if deadline < today:
                    expired_tasks.append(row[0])
            except Exception:
                continue
    if expired_tasks:
        messagebox.showwarning("Cảnh báo quá hạn", f"Bạn có {len(expired_tasks)} việc quá hạn:\n- " + "\n- ".join(expired_tasks[:3]))

# --- CÁC HÀM GIAO DIỆN ---

def xem_chi_tiet():
    if selected_id is None:
        return
    data = get_task_by_id(selected_id)
    if not data:
        return

    _, work, des, deadline_date, deadline_time, status, _ = data
    top = ttkb.Toplevel(root)
    top.title("Chi tiết công việc")
    top.geometry("400x300")
    for label, val in [("Việc", work), ("Mô tả", des), ("Hạn", f"{deadline_date} {deadline_time}"), ("Trạng thái", status)]:
        ttkb.Label(top, text=f"{label}: {val}", wraplength=350).pack(pady=5, padx=10)

def them():
    top = ttkb.Toplevel(root)
    form = DataEntryForm(top)
    # Ensure new tasks default to the currently selected date in the calendar view
    form.date_deadline.set(time_make)

    for w in form.winfo_children():
        if isinstance(w, ttk.Frame):
            for b in w.winfo_children():
                try:
                    if b.cget("text") == "Lưu":
                        b.configure(command=lambda: [form.on_submit(), show(), top.destroy()])
                except Exception:
                    pass

def sua():
    if selected_id is None:
        return
    data = get_task_by_id(selected_id)
    if not data:
        return

    _, work, des, deadline_date, deadline_time, status, important = data
    top = ttkb.Toplevel(root)
    form = DataEntryForm(top)
    form.work_name.set(work); form.work_des.set(des); form.date_deadline.set(deadline_date);

    time_str = deadline_time
    if ":" in time_str:
        h, m = time_str.split(":")
        form.hour.set(h)
        form.minute.set(m)

    imp_val = important
    if isinstance(imp_val, str) and imp_val.lower() == "false":
        form.important.set("0")
    elif str(imp_val).lower() in ("1", "true"):
        form.important.set("1")
    else:
        try:
            form.important.set(str(int(imp_val)))
        except (ValueError, TypeError):
            form.important.set("0")

    def do_update():
        update(
            selected_id, form.work_name.get(), form.work_des.get(), 
            form.date_deadline.get(), f"{form.hour.get()}:{form.minute.get()}", status, form.important.get())
        show()
        top.destroy()
        
    for w in form.winfo_children():
        if isinstance(w, ttk.Frame):
            for b in w.winfo_children():
                try:
                    if b.cget("text") == "Lưu":
                        b.configure(text="Cập nhật", command=do_update)
                except Exception:
                    pass

def hoan_thanh():
    global selected_id
    if selected_id is None:
        return
    d = get_task_by_id(selected_id)
    if not d:
        return
    _, work, des, deadline_date, deadline_time, _, important = d
    update(selected_id, work, des, deadline_date, deadline_time, "Hoàn thành", important)
    show()
    selected_id = None

def xoa():
    global selected_id
    if selected_id is not None:
        delete(selected_id)
        show()
        selected_id = None

def chon(event):
    global selected_id
    item = tree.selection()
    if item: selected_id = int(item[0])

# --- GIAO DIỆN CHÍNH ---
filter_frame = ttk.Frame(root); filter_frame.pack(pady=10)
ttkb.Label(filter_frame, text="Lọc:").pack(side=LEFT)
loc_box = ttk.Combobox(filter_frame, values=["Tất cả", "Chưa hoàn thành", "Hoàn thành"], state="readonly")
loc_box.current(0); loc_box.pack(side=LEFT, padx=5); loc_box.bind("<<ComboboxSelected>>", loc_du_lieu)

#can thay doi ngay bang cach dung nut lich
date_label = ttkb.Label(filter_frame, text=time_make)
date_label.pack(side=RIGHT)
ttk.Button(master=filter_frame, text="📅", command=open_calendar).pack(side=LEFT, padx=5)

# SỬA LỖI TẠI ĐÂY: Thêm 'text=' vào các hàm heading
tree = ttk.Treeview(root, columns=(1, 2, 3, 4), show="headings")
tree.heading(1, text="Công việc", anchor=W)
tree.heading(2, text="Deadline", anchor=CENTER)
tree.heading(3, text="Trạng thái", anchor=CENTER)
tree.heading(4, text="Quan trọng", anchor=CENTER)
# Align cell text to match header alignment
tree.column(1, width=200, anchor=W, stretch=YES)
tree.column(2, width=100, anchor=CENTER, stretch=YES)
tree.column(3, width=100, anchor=CENTER, stretch=YES)
tree.column(4, width=100, anchor=CENTER, stretch=YES)
tree.pack(fill=BOTH, expand=YES, padx=20)
tree.bind("<<TreeviewSelect>>", chon)

btn_frame = ttk.Frame(root); btn_frame.pack(pady=20)
for txt, cmd, style in [("👁 Xem", xem_chi_tiet, INFO), ("✚ Thêm", them, SUCCESS), 
                        ("✎ Sửa", sua, WARNING), ("✔ Hoàn thành", hoan_thanh, PRIMARY), ("✘ Xóa", xoa, DANGER)]:
    ttkb.Button(btn_frame, text=txt, command=cmd, bootstyle=style).pack(side=LEFT, padx=5)

show()
check_alerts()
root.mainloop()