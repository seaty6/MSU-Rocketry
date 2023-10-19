from umqtt.simple import MQTTClient
from machine import Pin
from time import sleep

# mqtt client setup
CLIENT_NAME = 'SolednoidESP'
BROKER_ADDR = '192.168.0.100'
mqttc = MQTTClient(CLIENT_NAME, BROKER_ADDR, keepalive=60)
mqttc.connect()

# button setup
btn = Pin(0)
BTN_TOPIC = CLIENT_NAME.encode() + b'/btn/0'
### -----------------------

# solenoid setup
sol1 = Pin(4, Pin.OUT)
sol2 = Pin(16, Pin.OUT)
sol3 = Pin(18, Pin.OUT)
ematch = Pin(19, Pin.OUT) #ematch!
soltopic = b'/solenoid'



def change_solenoid(topic, msg):
    if msg.decode() == 'sol1off':
        sol1.value(0)
    if msg.decode() == 'sol1on':
        sol1.value(1)
    if msg.decode() == 'sol2off':
        sol2.value(0)
    if msg.decode() == 'sol2on':
        sol2.value(1)  
    if msg.decode() == 'sol3off':
        sol3.value(0)
    if msg.decode() == 'sol3on':
        sol3.value(1)

    #ematch! 
    if msg.decode() == 'ematchoff':
        ematch.value(0)
    if msg.decode() == 'ematchon':
        ematch.value(1)
        
# mqtt subscriptions
mqttc.set_callback(change_solenoid)
mqttc.subscribe(soltopic)


while True:
    mqttc.publish( BTN_TOPIC, str(btn.value()).encode() )
    mqttc.check_msg()
    sleep(0.5)

