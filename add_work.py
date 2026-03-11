import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from calender import DatePickerDialog
import datetime
from database import write


class DataEntryForm(ttk.Frame):

    def __init__(self, master):
        super().__init__(master, padding=(20, 10))
        self.pack(fill=BOTH, expand=YES)

        # form variables
        self.work_name = ttk.StringVar(value="")
        self.work_des = ttk.StringVar(value="")
        self.date_deadline = ttk.StringVar(value="")
        self.hour = ttk.StringVar(value="00")
        self.minute = ttk.StringVar(value="00")
        self.important = ttk.IntVar(value=0)

        # form header
        hdr_txt = "Hãy nhập công việc cần làm" 
        hdr = ttk.Label(master=self, text=hdr_txt, width=50)
        hdr.pack(fill=X, pady=10)

        # form entries
        self.create_form_entry("Work", self.work_name)
        self.create_form_entry("Description", self.work_des)
        self.create_date_entry()
        self.create_time_entry()
        self.create_important_check()
        self.create_buttonbox()

    def create_form_entry(self, label, variable):
        """Create a single form entry"""
        container = ttk.Frame(self)
        container.pack(fill=X, expand=YES, pady=5)

        lbl = ttk.Label(master=container, text=label.title(), width=10)
        lbl.pack(side=LEFT, padx=5)

        ent = ttk.Entry(master=container, textvariable=variable)
        ent.pack(side=LEFT, padx=5, fill=X, expand=YES)

    def _validate_hour(self, value):
        if value == "":
            return True
        try:
            return 0 <= int(value) <= 23
        except ValueError:
            return False

    def _validate_minute(self, value):
        if value == "":
            return True
        try:
            return 0 <= int(value) <= 59
        except ValueError:
            return False
        
    def create_date_entry(self):
        container = ttk.Frame(self)
        container.pack(fill=X, expand=YES, pady=5)

        lbl = ttk.Label(master=container, text="Date", width=12)
        lbl.pack(side=LEFT, padx=5)

        ent = ttk.Entry(master=container, textvariable=self.date_deadline, state="readonly")
        ent.pack(side=LEFT, padx=5, fill=X, expand=YES)
        
        btn = ttk.Button(master=container, text="📅", command=self.open_calendar)
        btn.pack(side=LEFT, padx=5)

    def open_calendar(self):
        dialog = DatePickerDialog(
            parent=self.master,
            title="Choose a Date",
            firstweekday=0, # Start on Monday
            startdate=datetime.date.today(),
            bootstyle=PRIMARY
        )
        selected = dialog.date_selected
        
        if selected:
            selected_str = f"{selected.strftime('%d/%m/%Y')}"
            self.date_deadline.set(selected_str)
            
    def create_time_entry(self):
        container = ttk.Frame(self)
        container.pack(fill=X, expand=YES, pady=5)

        lbl = ttk.Label(master=container, text="Deadline", width=12)
        lbl.pack(side=LEFT, padx=5)

        vcmd_h = (self.register(self._validate_hour), "%P")
        hour_spin = ttk.Spinbox(
            master=container, from_=0, to=23, textvariable=self.hour,
            width=3, format="%02.0f", wrap=True,
            validate="key", validatecommand=vcmd_h
        )
        hour_spin.pack(side=LEFT, padx=(5, 0))

        sep = ttk.Label(master=container, text=":")
        sep.pack(side=LEFT)

        vcmd_m = (self.register(self._validate_minute), "%P")
        min_spin = ttk.Spinbox(
            master=container, from_=0, to=59, textvariable=self.minute,
            width=3, format="%02.0f", wrap=True,
            validate="key", validatecommand=vcmd_m
        )
        min_spin.pack(side=LEFT, padx=(0, 5))

    def create_important_check(self):
        container = ttk.Frame(self)
        container.pack(fill=X, expand=YES, pady=5)

        lbl = ttk.Label(master=container, text="Important", width=12)
        lbl.pack(side=LEFT, padx=5)

        chk = ttk.Checkbutton(master=container, variable=self.important, bootstyle="danger-round-toggle")
        chk.pack(side=LEFT, padx=5)

    def create_buttonbox(self):
        """Create the application buttonbox"""
        container = ttk.Frame(self)
        container.pack(fill=X, expand=YES, pady=(15, 10))

        sub_btn = ttk.Button(
            master=container,
            text="Submit",
            command=self.on_submit,
            bootstyle=SUCCESS,
            width=6,
        )
        sub_btn.pack(side=RIGHT, padx=5)
        sub_btn.focus_set()

        cnl_btn = ttk.Button(
            master=container,
            text="Cancel",
            command=self.on_cancel,
            bootstyle=DANGER,
            width=6,
        )
        cnl_btn.pack(side=RIGHT, padx=5)
    

    def on_submit(self):
        time_str = f"{self.hour.get()}:{self.minute.get()}"
        date_str = self.date_deadline.get()
        work_name = self.work_name.get()
        status = "Chưa hoàn thành"
        des = self.des.get() if hasattr(self, 'des') else ""
        
        task_data = (work_name, des, date_str, time_str, status)
        
        write(task_data)
        
        if hasattr(self, 'on_save') and self.on_save:
            self.on_save()
        self.master.destroy()

    def on_cancel(self):
        self.master.destroy()

    def on_cancel(self):
        """Cancel and close the application."""
        self.quit()


if __name__ == "__main__":

    app = ttk.Window("Data Entry", "superhero", resizable=(False, False))
    DataEntryForm(app)
    app.mainloop()