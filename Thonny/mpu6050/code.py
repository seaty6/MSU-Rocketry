import time
import board
import os
import ssl
import socketpool
import wifi
import adafruit_minimqtt.adafruit_minimqtt as MQTT

import adafruit_mpu6050

def connect(mqtt_client, userdata, flags, rc):
    # This function will be called when the mqtt_client is connected successfully to the broker.
    print("Connected to MQTT Broker!")


def disconnect(mqtt_client, userdata, rc):
    # This method is called when the mqtt_client disconnects from the broker.
    print("Disconnected from MQTT Broker!")
    
    
# Connect to WiFi
wifi.radio.connect(os.getenv("CIRCUITPY_WIFI_SSID"), os.getenv("CIRCUITPY_WIFI_PASSWORD"))

# Create a socket pool
pool = socketpool.SocketPool(wifi.radio)

# Set up a MiniMQTT Client
mqtt_client = MQTT.MQTT(
    broker="192.168.0.100",
    port=1883,
    username="RocketryMQTTAP",
    password="gospartans",
    socket_pool=pool,
    ssl_context=ssl.create_default_context(),
)

mqtt_client.connect()

i2c = board.I2C() # uses board.SCL and board.SDA
#i2c = board.STEMMA_I2C() # For using the built-in STEMMA QT connector on a microcontroller
mpu = adafruit_mpu6050.MPU6050(i2c)

while True:
    #print("Gyro X:%.2f, Y: %.2f, Z: %.2f rad/s" % (mpu.gyro))
    #print("Temperature: %.2f C" % mpu.temperature)
    
    mqtt_client.publish(topic="mpu6050/AcX", msg=str( mpu.acceleration[0] ))
    mqtt_client.publish(topic="mpu6050/AcY", msg=str( mpu.acceleration[1] ))
    time.sleep(0.5)
