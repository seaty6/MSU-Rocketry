import time  # Don't forget to import the time module

CLIENT_NAME = 'loadcellesp_01'
BROKER_ADDR = '192.168.0.100'
mqttc = MQTTClient(CLIENT_NAME, BROKER_ADDR, keepalive=60)
mqttc.connect()

pin_OUT = Pin(18, Pin.IN, pull=Pin.PULL_DOWN)
pin_SCK = Pin(4, Pin.OUT)

# Use the GPIO constructor
hx = HX711(pin_SCK, pin_OUT, gain = 64)
hx.tare()

while True:
    value = hx.read()
    print("HX Read:" , value)
    value = hx.get_value()
    mqttc.publish( b'/loadcell/force/', str(value).encode() )
    print("HX Get Value:", value)
    time.sleep(0.20)
