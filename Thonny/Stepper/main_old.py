from stepper import Stepper
from machine import ADC, Pin
import time

s1 = Stepper(26,27,steps_per_rev=200,speed_sps=50)

#Step Pin: 26
#Direciton Pin: 27
rest = Pin(25, Pin.OUT)
#Rest Pin: 25 

rest.value(1)
print(s1.is_enabled())
s1.target_deg(360)
time.sleep(5.0)
s1.target_deg(0)
time.sleep(5.0)
print("done")

rest.value(0)
print("started")
print(s1.is_enabled())
s1.target_deg(360)
time.sleep(5.0)
s1.target_deg(0)
time.sleep(5.0)
print("done")
