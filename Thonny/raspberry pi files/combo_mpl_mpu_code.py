import time
import board

import os
import ssl
import socketpool
import wifi
import adafruit_minimqtt.adafruit_minimqtt as MQTT

import adafruit_mpl3115a2
import adafruit_mpu6050


############# MQTT SETUP STUFF #############
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

############################################

# Create sensor object, communicating over the board's default I2C bus
i2c = board.I2C()  # uses board.SCL and board.SDA

# Initialize the MPL3115A2.
sensor = adafruit_mpl3115a2.MPL3115A2(i2c)
sensor.sealevel_pressure = 1022.5  # Look up the pressure at sealevel at the specific time/location in hectopascals

# Initialize the MPU6050
mpu = adafruit_mpu6050.MPU6050(i2c)


while True:
    mqtt_client.publish(topic="mpl3115a2/altitude", msg=str( sensor.altitude ))
    mqtt_client.publish(topic="mpl3115a2/temperature", msg=str( sensor.temperature ))
    
    mqtt_client.publish(topic="mpu6050/AcX", msg=str( mpu.acceleration[0] ))
    mqtt_client.publish(topic="mpu6050/AcY", msg=str( mpu.acceleration[1] ))
    time.sleep(0.5)
