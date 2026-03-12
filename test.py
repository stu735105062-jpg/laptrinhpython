import datetime 
import time

now = time.localtime()
year,month,day,hour,minue,second,*_= now


print(f'{hour}:{minue}')