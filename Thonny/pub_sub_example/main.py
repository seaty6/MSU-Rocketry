from umqtt.simple import MQTTClient
from machine import Pin
from time import sleep

# mqtt client setup
CLIENT_NAME = 'esp01'
BROKER_ADDR = '192.168.0.100'
mqttc = MQTTClient(CLIENT_NAME, BROKER_ADDR, keepalive=60)
mqttc.connect()

# button setup
btn = Pin(0)
BTN_TOPIC = CLIENT_NAME.encode() + b'/btn/0'
### -----------------------

# led setup
led = Pin(2, Pin.OUT)
LED_TOPIC = b'/led/0'

def blink_led(topic, msg):
    if msg.decode() == '1':
        led.value(0)
    else:
        led.value(1)
        
# mqtt subscription
mqttc.set_callback(blink_led)
mqttc.subscribe(LED_TOPIC)

while True:
    mqttc.publish( BTN_TOPIC, str(btn.value()).encode() )
    mqttc.check_msg()
    sleep(0.5)