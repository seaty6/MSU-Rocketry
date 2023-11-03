import time
import board

import os
import ssl
import socketpool
import paho.mqtt.client as mqtt

from mpl3115a2 import adafruit_mpl3115a2
from mpu6050 import adafruit_mpu6050

client_name = "SpartanFlight"
server_address = "raspberrypi"
mqtt_client = mqtt.Client(client_name)

mqtt_client.connect(server_address, 1883, 60)

############################################

# Create sensor object, communicating over the board's default I2C bus
i2c = board.I2C()  # uses board.SCL and board.SDA

# Initialize the MPL3115A2.
sensor = adafruit_mpl3115a2.MPL3115A2(i2c)
sensor.sealevel_pressure = 1022.5  # Look up the pressure at sealevel at the specific time/location in hectopascals

# Initialize the MPU6050
mpu = adafruit_mpu6050.MPU6050(i2c)


while True:
    mqtt_client.publish("mpl3115a2/altitude", str( sensor.altitude ))
    mqtt_client.publish("mpl3115a2/temperature", str( sensor.temperature ))
    
    mqtt_client.publish("mpu6050/AcX", str( mpu.acceleration[0] ))
    mqtt_client.publish("mpu6050/AcY", str( mpu.acceleration[1] ))
    time.sleep(0.5)
