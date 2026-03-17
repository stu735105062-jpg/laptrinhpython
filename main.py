from database import *
from tkinter import *
from tkinter import ttk,messagebox
import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
from add_work import DataEntryForm
from calender import DatePickerDialog
import datetime 
import time
from windows_toasts import Toast, WindowsToaster
from heapq import nlargest

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

now = time.localtime()
year,month,day,*_= now
make_time = datetime.date(year=year,month=month,day=day)

time_make = make_time.strftime("%d/%m/%Y")

work_waitlist = {}
for_later_waitlist = {}

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
    global work_waitlist
    for i in tree.get_children(): tree.delete(i)
    data = get_work_by_date(time_make)
    today = datetime.datetime.now()
    
    work_waitlist.clear()
    today_str = today.strftime("%d/%m/%Y")
    today_data = get_work_by_date(today_str)
    
    for row in today_data:
        # id, work, des, date, time, status, important
        if row[5] == "Chưa hoàn thành":
            id_work = row[0]
            new_work = (row[1], row[4])
            work_waitlist[new_work] = id_work

    for row in data:
        db_id = row[0]
        if filter_val == "Tất cả" or row[5] == filter_val:
            is_expired = False
            if row[5] == "Chưa hoàn thành":
                try:
                    deadline = datetime.datetime.strptime(row[3], '%d/%m/%Y')
                    if deadline.date() < today.date():
                        is_expired = True
                except: pass
            
            if row[6] == 1:
                row[6] = 'Có'
            else:
                row[6] = 'Không'

            iid = tree.insert('', END, iid=db_id, values=(row[1],row[4], row[5], row[6]))
            
            if is_expired:
                tree.item(iid, tags=('expired',))
    
    tree.tag_configure('expired', foreground='#FF5555', font=('Arial', 10, 'bold'))

notified_tasks = set()

def time_to_noti():
    if not work_waitlist:
        root.after(1000, time_to_noti)
        return

    now_time = datetime.datetime.now()
    current_time_str = now_time.strftime("%H:%M")

    for (work, task_time), task_id in list(work_waitlist.items()):
        if task_time == current_time_str and task_id not in notified_tasks:
            noti(work)
            notified_tasks.add(task_id)

    root.after(1000, time_to_noti)

def loc_du_lieu(event):
    show(loc_box.get())

def noti(content):
    title = WindowsToaster('Nhắc việc')
    new_toast = Toast()
    new_toast.text_fields = [content]
    try:
        title.show_toast(new_toast)
    except: pass

# --- CÁC HÀM GIAO DIỆN ---

def xem_chi_tiet():
    if selected_id is None: return
    data = get_work_by_id(selected_id)
    if not data: return
    top = ttkb.Toplevel(root)
    top.title("Chi tiết công việc")
    top.geometry("400x300")
    for label, val in [("Việc", data[0]), ("Mô tả", data[1]), ("Hạn", f"{data[2]} {data[3]}"), ("Trạng thái", data[4])]:
        ttkb.Label(top, text=f"{label}: {val}", wraplength=350).pack(pady=5, padx=10)

def them():
    top = ttkb.Toplevel(root)
    form = DataEntryForm(top)
    
    def on_add_save():
        if form.on_submit() is not False:
            show()
            top.destroy()
            
    for w in form.winfo_children():
        if isinstance(w, ttk.Frame):
            for b in w.winfo_children():
                try:
                    if b.cget("text") == "Lưu":
                        b.configure(command=on_add_save)
                except Exception:
                    pass

def sua():
    if selected_id is None: return
    data = get_work_by_id(selected_id)
    if not data: return
    top = ttkb.Toplevel(root)
    form = DataEntryForm(top)
    form.work_name.set(data[0]); form.work_des.set(data[1]); form.date_deadline.set(data[2]); 
    
    time_str = data[3]
    if ":" in time_str:
        h, m = time_str.split(":")
        form.hour.set(h)
        form.minute.set(m)
    
    imp_val = data[5]
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
        if form.work_name.get() == "":
            messagebox.showerror("Lỗi", "Vui lòng nhập tên công việc", parent=top)
            return
            
        update(
            selected_id,form.work_name.get(),form.work_des.get(), 
            form.date_deadline.get(),f"{form.hour.get()}:{form.minute.get()}",data[4],form.important.get())
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
    if selected_id is None: return
    d = get_work_by_id(selected_id)
    if not d: return
    
    if d[4] == "Chưa hoàn thành":
        update(selected_id, d[0], d[1], d[2], d[3], "Hoàn thành", d[5])
        show()
    else:
        update(selected_id, d[0], d[1], d[2], d[3], "Chưa hoàn thành", d[5])
        show()

def xoa():
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
tree.heading(1, text="Công việc")
tree.heading(2, text="Deadline")
tree.heading(3, text="Trạng thái")
tree.heading(4, text="Quan trọng")
tree.column(1, width=200); tree.column(2, width=100); tree.column(3, width=100), tree.column(4, width=100)
tree.pack(fill=BOTH, expand=YES, padx=20)
tree.bind("<<TreeviewSelect>>", chon)

btn_frame = ttk.Frame(root); btn_frame.pack(pady=20)
for txt, cmd, style in [("👁 Xem", xem_chi_tiet, INFO), ("✚ Thêm", them, SUCCESS), 
                        ("✎ Sửa", sua, WARNING), ("✔ Trạng thái", hoan_thanh, PRIMARY), ("✘ Xóa", xoa, DANGER)]:
    ttkb.Button(btn_frame, text=txt, command=cmd, bootstyle=style).pack(side=LEFT, padx=5)

show()
time_to_noti()
root.mainloop()