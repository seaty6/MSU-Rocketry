from umqtt.simple import MQTTClient
from machine import Pin
from time import sleep

### --- same as before ---
CLIENT_NAME = 'esp01'
BROKER_ADDR = '192.168.0.100'
mqttc = MQTTClient(CLIENT_NAME, BROKER_ADDR, keepalive=60)
mqttc.connect()
### ----------------------

# button setup
btn = Pin(0)
BTN_TOPIC = CLIENT_NAME.encode() + b'/btn/0'

while True:
	mqttc.publish( BTN_TOPIC, str(btn.value()).encode() )
	sleep(0.5)