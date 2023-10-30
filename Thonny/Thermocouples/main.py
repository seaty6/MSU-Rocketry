from max6675 import MAX6675
from machine import Pin, I2C
from umqtt.simple import MQTTClient
import time

CLIENT_NAME = 'espthermo'
BROKER_ADDR = '192.168.0.100'
mqttc = MQTTClient(CLIENT_NAME, BROKER_ADDR, keepalive=60)
mqttc.connect()

so = Pin(19, Pin.IN)
sck = Pin(5, Pin.OUT)
cs = Pin(23, Pin.OUT)

max = MAX6675(sck, cs , so)

for _ in range(1000):
    # print(max.read())
    mqttc.publish( b'/thermometer/sensor', str( max.read() ).encode() )
    time.sleep(1)