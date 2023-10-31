from machine import Pin
from hx711 import HX711
from umqtt.simple import MQTTClient
import time  # Don't forget to import the time module

CLIENT_NAME = 'loadcellesp_01'
BROKER_ADDR = '192.168.0.100'
mqttc = MQTTClient(CLIENT_NAME, BROKER_ADDR, keepalive=60)
mqttc.connect()

pin_OUT1 = Pin(18, Pin.IN, pull=Pin.PULL_DOWN)
pin_OUT2 = Pin(19, Pin.IN, pull=Pin.PULL_DOWN)
pin_OUT3 = Pin(21, Pin.IN, pull=Pin.PULL_DOWN)

pin_SCK1 = Pin(4, Pin.OUT)
pin_SCK2 = Pin(22, Pin.OUT)
pin_SCK3 = Pin(23, Pin.OUT)

# Use the GPIO constructor
hx1 = HX711(pin_SCK1, pin_OUT1, gain = 64)
hx2 = HX711(pin_SCK2, pin_OUT2, gain = 64)
hx3 = HX711(pin_SCK3, pin_OUT3, gain = 64)

while True:
    value1 = hx1.get_value()
    value2 = hx2.get_value()
    value3 = hx3.get_value()
    mqttc.publish( b'/loadcell/force1/', str(value1).encode() )
    mqttc.publish( b'/loadcell/force2/', str(value2).encode() )
    mqttc.publish( b'/loadcell/force3/', str(value3).encode() )
    print("HX Get Value1:", value1)
    print("HX Get Value2:", value2)
    print("HX Get Value3:", value3)
    time.sleep(0.25)

