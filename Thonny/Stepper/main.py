from umqtt.simple import MQTTClient
from stepper import Stepper
from machine import Pin
from time import sleep

# mqtt client setup
CLIENT_NAME = 'StepperESP'
BROKER_ADDR = '192.168.0.100'
mqttc = MQTTClient(CLIENT_NAME, BROKER_ADDR, keepalive=60)
mqttc.connect()

# Stepper setup
s1 = Stepper(26,27,steps_per_rev=200,speed_sps=50)
rest = Pin(25, Pin.OUT)

steptopic = b'/stepper'

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def move_stepper(topic, msg):

    if is_number(msg.decode()):
        s1.target_deg(float(msg.decode()))
    if msg.decode() == 'stoprest':
        rest.value(1)
    if msg.decode() == 'startrest':
        rest.value(0)
    
        
# mqtt subscription
mqttc.set_callback(move_stepper)
mqttc.subscribe(steptopic)


while True:
    mqttc.check_msg()
    sleep(0.25)

