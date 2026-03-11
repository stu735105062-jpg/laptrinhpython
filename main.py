from database import *
from tkinter import *
from tkinter import ttk, messagebox
import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
from add_work import DataEntryForm
from datetime import datetime

connect()
root = ttkb.Window(themename="superhero")
root.title("Quản lý công việc chuyên nghiệp")
root.geometry("800x700")

selected_index = None

# --- CÁC HÀM XỬ LÝ DỮ LIỆU ---

def show(filter_val="Tất cả"):
    for i in tree.get_children(): tree.delete(i)
    data = read()
    today = datetime.now()
    
    for idx, row in enumerate(data):
        # row: [work, des, date, time, status]
        if filter_val == "Tất cả" or row[4] == filter_val:
            is_expired = False
            if row[4] == "Chưa hoàn thành":
                try:
                    deadline = datetime.strptime(row[2], '%d/%m/%Y')
                    if deadline < today and deadline.date() != today.date():
                        is_expired = True
                except: pass
            
            iid = tree.insert('', END, iid=idx, values=(row[0], row[2], row[4]))
            if is_expired:
                tree.item(iid, tags=('expired',))
    
    tree.tag_configure('expired', foreground='#FF5555', font=('Arial', 10, 'bold'))

def loc_du_lieu(event):
    show(loc_box.get())

def check_alerts():
    today = datetime.now()
    expired_tasks = []
    for row in read():
        if row[4] == "Chưa hoàn thành":
            try:
                deadline = datetime.strptime(row[2], '%d/%m/%Y')
                if deadline < today and deadline.date() != today.date():
                    expired_tasks.append(row[0])
            except: continue
    if expired_tasks:
        messagebox.showwarning("Cảnh báo quá hạn", f"Bạn có {len(expired_tasks)} việc quá hạn:\n- " + "\n- ".join(expired_tasks[:3]))

# --- CÁC HÀM GIAO DIỆN ---

def xem_chi_tiet():
    if selected_index is None: return
    data = read()[selected_index]
    top = ttkb.Toplevel(root)
    top.title("Chi tiết công việc")
    top.geometry("400x300")
    for label, val in [("Việc", data[0]), ("Mô tả", data[1]), ("Hạn", f"{data[2]} {data[3]}"), ("Trạng thái", data[4])]:
        ttkb.Label(top, text=f"{label}: {val}", wraplength=350).pack(pady=5, padx=10)

def them():
    top = ttkb.Toplevel(root)
    form = DataEntryForm(top)
    for w in form.winfo_children():
        if isinstance(w, ttk.Frame):
            for b in w.winfo_children():
                try:
                    if b.cget("text") == "Lưu":
                        b.configure(command=lambda: [form.on_submit(), show(), top.destroy()])
                except Exception:
                    pass

def sua():
    if selected_index is None: return
    data = read()[selected_index]
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
        update(
            selected_index,form.work_name.get(),form.work_des.get(), 
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
    global selected_index
    if selected_index is None: return
    d = read()[selected_index]
    # preserve the "important" flag when marking as completed
    imp_val = d[5] if len(d) > 5 else "0"
    update(selected_index, d[0], d[1], d[2], d[3], "Hoàn thành", imp_val)
    # refresh list and clear selection so the user knows nothing is selected
    show()
    selected_index = None

def xoa():
    if selected_index is not None:
        delete(selected_index)
        show()

def chon(event):
    global selected_index
    item = tree.selection()
    if item: selected_index = int(item[0])

# --- GIAO DIỆN CHÍNH ---
filter_frame = ttk.Frame(root); filter_frame.pack(pady=10)
ttkb.Label(filter_frame, text="Lọc:").pack(side=LEFT)
loc_box = ttk.Combobox(filter_frame, values=["Tất cả", "Chưa hoàn thành", "Hoàn thành"], state="readonly")
loc_box.current(0); loc_box.pack(side=LEFT, padx=5); loc_box.bind("<<ComboboxSelected>>", loc_du_lieu)

# SỬA LỖI TẠI ĐÂY: Thêm 'text=' vào các hàm heading
# Configure columns with center alignment and allow them to stretch
tree = ttk.Treeview(root, columns=(1, 2, 3), show="headings")
tree.heading(1, text="Công việc", anchor=CENTER)
tree.heading(2, text="Deadline", anchor=CENTER)
tree.heading(3, text="Trạng thái", anchor=CENTER)
# set initial widths and allow stretching so the table fills the window
tree.column(1, width=250, minwidth=120, anchor=CENTER, stretch=YES)
tree.column(2, width=120, minwidth=80, anchor=CENTER, stretch=YES)
tree.column(3, width=120, minwidth=80, anchor=CENTER, stretch=YES)
tree.pack(fill=BOTH, expand=YES, padx=20, pady=5)
tree.bind("<<TreeviewSelect>>", chon)

btn_frame = ttk.Frame(root); btn_frame.pack(pady=20)
for txt, cmd, style in [("👁 Xem", xem_chi_tiet, INFO), ("✚ Thêm", them, SUCCESS), 
                        ("✎ Sửa", sua, WARNING), ("✔ Hoàn thành", hoan_thanh, PRIMARY), ("✘ Xóa", xoa, DANGER)]:
    ttkb.Button(btn_frame, text=txt, command=cmd, bootstyle=style).pack(side=LEFT, padx=5)

show()
check_alerts()
root.mainloop()