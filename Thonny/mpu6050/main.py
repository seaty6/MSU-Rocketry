from machine import I2C, Pin
import mpu6050
import time
from umqtt.simple import MQTTClient
 
CLIENT_NAME = 'espaltimeter'
BROKER_ADDR = '192.168.137.207'
mqttc = MQTTClient(CLIENT_NAME, BROKER_ADDR, keepalive=60)
mqttc.connect()
 
i2c = I2C(scl=Pin(22), sda=Pin(21))     #initializing the I2C method for ESP32
#i2c = I2C(scl=Pin(5), sda=Pin(4))       #initializing the I2C method for ESP8266
mpu= mpu6050.accel(i2c)
 
while True:
     dic = mpu.get_values()
     
     offsets = mpu.calibrate(dic)  # comment this to get back to uncalibrated values
    
     mqttc.publish( b'/mpu6050/AcX/', str( dic["AcX"] ).encode() )
     mqttc.publish( b'/mpu6050/AcY/', str( dic["AcY"] ).encode() )
     mqttc.publish( b'/mpu6050/AcZ/', str( dic["AcZ"] ).encode() )
     time.sleep(0.5)