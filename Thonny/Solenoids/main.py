from umqtt.simple import MQTTClient
from machine import Pin
from time import sleep

# mqtt client setup
CLIENT_NAME = 'esp01'
BROKER_ADDR = '192.168.137.86'
mqttc = MQTTClient(CLIENT_NAME, BROKER_ADDR, keepalive=60)
mqttc.connect()

# button setup
btn = Pin(0)
BTN_TOPIC = CLIENT_NAME.encode() + b'/btn/0'
### -----------------------

# led setup
sol1 = Pin(2, Pin.OUT)
sol2 = Pin(4, Pin.OUT)
soltopic = b'/solenoid/1'



def change_solenoid(topic, msg):
    if msg.decode() == 'sol1off':
        sol1.value(0)
    if msg.decode() == 'sol1on':
        sol1.value(1)
    if msg.decode() == 'sol2off':
        sol2.value(0)
    if msg.decode() == 'sol2on':
        sol2.value(1)  
        
# mqtt subscription
mqttc.set_callback(change_solenoid)
mqttc.subscribe(soltopic)


while True:
    mqttc.publish( BTN_TOPIC, str(btn.value()).encode() )
    mqttc.check_msg()
    sleep(0.5)

