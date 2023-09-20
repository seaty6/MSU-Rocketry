from machine import Pin
from time import sleep

led = Pin(2, Pin.OUT)

for i in range(10):
    led.value(1)
    sleep(1)
    led.value(0)
    sleep(1)
    