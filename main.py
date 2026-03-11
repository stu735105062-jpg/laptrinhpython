from database import *
from tkinter import *
from tkinter import ttk
from datetime import *
import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
from calender import DatePickerDialog
from add_work import DataEntryForm

connect()

selected_index = None

# chọn ngày
def mo_lich():
    dialog = DatePickerDialog(
        parent=root,
        title="Choose a Date",
        firstweekday=0, # Start on Monday
        startdate=date.today(),
        bootstyle=PRIMARY
    )
    selected = dialog.date_selected
    
    if selected:
        selected = f"{selected.strftime('%B %d, %Y')}"
        deadline.set(selected)
    else:
        return

def add_work():
    top = ttkb.Toplevel(root)
    top.title("Add Work")
    top.resizable(False, False)
    DataEntryForm(top)


# hiển thị
def show():

    for i in tree.get_children():
        tree.delete(i)

    cv = read()

    for i in cv:
        tree.insert('',END,values=i)


# xoá
def xoa():
    global selected_index

    if selected_index!=None:
        delete(selected_index)
        show()


# sửa
def sua():
    global selected_index

    if selected_index!=None:
        line = task.get()+'-'+deadline.get()+'-'+status.get()
        update(selected_index,line)
        show()


# chọn item
def chon(event):
    global selected_index

    item = tree.selection()

    if item:
        selected_index = tree.index(item)

        data = tree.item(item)['values']

        task.set(data[0])
        deadline.set(data[1])
        status.set(data[2])


# lọc trạng thái
def loc():

    for i in tree.get_children():
        tree.delete(i)

    cv = read()

    for i in cv:
        if i[2] == loc_status.get():
            tree.insert('',END,values=i)


# nhắc việc quá hạn
def nhac_viec():

    for i in tree.get_children():
        tree.delete(i)

    today = date.today()

    cv = read()

    for i in cv:

        if i[2] == "Hoàn thành":
            continue

        try:
            d = datetime.strptime(i[1],"%d/%m/%Y").date()

            if d < today:
                tree.insert('',END,values=("QUÁ HẠN: "+i[0],i[1],i[2]))

        except:
            pass


# GUI
root = Tk()
root.title("Quản lý công việc")
root.geometry("650x550")

task = StringVar()
deadline = StringVar()
status = StringVar(value="Chưa hoàn thành")
loc_status = StringVar()

Label(root,text="QUẢN LÝ CÔNG VIỆC",
      font=("Arial",18,"bold")).pack(pady=10)

# bảng
frm = Frame(root)
frm.pack()

tree = ttk.Treeview(frm,columns=(1,2,3),show="headings",height=8)

tree.heading(1,text="Công việc")
tree.heading(2,text="Deadline")
tree.heading(3,text="Trạng thái")

tree.pack()

tree.bind("<<TreeviewSelect>>",chon)

# lọc
filter_frame = Frame(root)
filter_frame.pack(pady=10)

Label(filter_frame,text="Lọc trạng thái").pack(side=LEFT)

loc_box = ttk.Combobox(filter_frame,
                       textvariable=loc_status,
                       width=20,
                       state="readonly")

loc_box['values'] = ("Chưa hoàn thành","Đang làm","Hoàn thành")
loc_box.pack(side=LEFT,padx=5)

Button(filter_frame,text="Lọc",command=loc).pack(side=LEFT)

# nút chức năng
btn = Frame(root)
btn.pack(pady=10)

Button(btn,text="Thêm",width=10,command=add_work).pack(side=LEFT,padx=5)
Button(btn,text="Sửa",width=10,command=sua).pack(side=LEFT,padx=5)
Button(btn,text="Xoá",width=10,command=xoa).pack(side=LEFT,padx=5)
Button(btn,text="Xem",width=10,command=show).pack(side=LEFT,padx=5)
Button(btn,text="Nhắc việc",width=10,command=nhac_viec).pack(side=LEFT,padx=5)

show()

root.mainloop()