import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from calender import DatePickerDialog
import datetime
from database import write

class DataEntryForm(ttk.Frame):
    def __init__(self, master, on_save_callback=None):
        super().__init__(master, padding=(20, 10))
        self.pack(fill=BOTH, expand=YES)
        self.on_save = on_save_callback

        self.work_name = ttk.StringVar(value="")
        self.work_des = ttk.StringVar(value="")
        self.date_deadline = ttk.StringVar(value=datetime.date.today().strftime('%d/%m/%Y'))
        self.hour = ttk.StringVar(value="00")
        self.minute = ttk.StringVar(value="00")

        hdr_txt = "Hãy nhập công việc cần làm" 
        ttk.Label(master=self, text=hdr_txt, font=("Arial", 12, "bold")).pack(pady=10)

        self.create_form_entry("Công việc", self.work_name)
        self.create_form_entry("Mô tả", self.work_des)
        self.create_date_entry()
        self.create_time_entry()
        self.create_buttonbox()

    def create_form_entry(self, label, variable):
        container = ttk.Frame(self)
        container.pack(fill=X, expand=YES, pady=5)
        ttk.Label(master=container, text=label, width=10).pack(side=LEFT, padx=5)
        ttk.Entry(master=container, textvariable=variable).pack(side=LEFT, padx=5, fill=X, expand=YES)

    def create_date_entry(self):
        container = ttk.Frame(self)
        container.pack(fill=X, expand=YES, pady=5)
        ttk.Label(master=container, text="Ngày", width=10).pack(side=LEFT, padx=5)
        ttk.Entry(master=container, textvariable=self.date_deadline, state="readonly").pack(side=LEFT, padx=5, fill=X, expand=YES)
        ttk.Button(master=container, text="📅", command=self.open_calendar).pack(side=LEFT, padx=5)

    def open_calendar(self):
        dialog = DatePickerDialog(parent=self.master)
        if dialog.date_selected:
            self.date_deadline.set(dialog.date_selected.strftime('%d/%m/%Y'))

    def create_time_entry(self):
        container = ttk.Frame(self)
        container.pack(fill=X, expand=YES, pady=5)
        ttk.Label(master=container, text="Giờ", width=10).pack(side=LEFT, padx=5)
        ttk.Spinbox(container, from_=0, to=23, textvariable=self.hour, width=5).pack(side=LEFT, padx=5)
        ttk.Label(container, text=":").pack(side=LEFT)
        ttk.Spinbox(container, from_=0, to=59, textvariable=self.minute, width=5).pack(side=LEFT, padx=5)

    def create_buttonbox(self):
        container = ttk.Frame(self)
        container.pack(fill=X, expand=YES, pady=(15, 10))
        ttk.Button(container, text="Lưu", command=self.on_submit, bootstyle=SUCCESS).pack(side=RIGHT, padx=5)
        ttk.Button(container, text="Hủy", command=self.master.destroy, bootstyle=DANGER).pack(side=RIGHT, padx=5)

    def on_submit(self):
        task_data = (
            self.work_name.get(),
            self.work_des.get(),
            self.date_deadline.get(),
            f"{self.hour.get()}:{self.minute.get()}",
            "Chưa hoàn thành"
        )
        write(task_data)
        if self.on_save:
            self.on_save()
        self.master.destroy()