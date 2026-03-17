from windows_toasts import Toast, WindowsToaster
import time
import datetime

#toaster = WindowsToaster('Nhac viec')
#newToast = Toast()
#newToast.text_fields = ['Hello, world!']
#newToast.on_activated = lambda _: print('Toast clicked!')
#toaster.show_toast(newToast)

now = time.localtime()
y,m,d,hour,minute,sec,*_= now
time = datetime.time(hour=hour,minute=minute,second=sec)
print(hour)
print(minute)
print(sec)
print(time)
