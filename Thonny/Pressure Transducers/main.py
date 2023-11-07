
from machine import Pin, ADC
from umqtt.simple import MQTTClient
from time import sleep

CLIENT_NAME = 'esppressure'
BROKER_ADDR = '192.168.0.100'
mqttc = MQTTClient(CLIENT_NAME, BROKER_ADDR, keepalive=60)
mqttc.connect()

pot = ADC(Pin(34))
pot2 = ADC(Pin(35))
pot.atten(ADC.ATTN_11DB)
pot2.atten(ADC.ATTN_11DB) #Full range: 3.3v

while True:
  pot_value = pot.read()
  pot2_value = pot2.read()
  
  print(pot_value)
  mqttc.publish( b'/pressure/1', str( pot_value ).encode() )
  
  print(pot2_value)
  mqttc.publish( b'/pressure/2', str( pot2_value ).encode() )
  
  sleep(0.25)
