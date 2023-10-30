from umqtt.simple import MQTTClient
from machine import Pin, I2C
import time
from micropython_mpl3115a2 import mpl3115a2

### --- same as before ---
CLIENT_NAME = 'espaltimeter'
BROKER_ADDR = '192.168.137.254'
mqttc = MQTTClient(CLIENT_NAME, BROKER_ADDR, keepalive=60)
mqttc.connect()
### ----------------------

i2c = I2C(1, sda=Pin(21), scl=Pin(22))  # Correct I2C pins for RP2040
mpl = mpl3115a2.MPL3115A2(i2c)

while True:
	mqttc.publish( b'/altimeter/pressure/', str( mpl.pressure ).encode() )
	mqttc.publish( b'/altimeter/altitude/', str( mpl.altitude ).encode() )
	mqttc.publish( b'/altimeter/temperature/', str( mpl.temperature ).encode() )
	time.sleep(0.5)`
