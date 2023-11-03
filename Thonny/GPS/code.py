import time
import board
import busio

import paho.mqtt.client as mqtt

import adafruit_gps


############# MQTT SETUP STUFF #############

client_name = "SpartanFlight"
server_address = "raspberrypi"
mqtt_client = mqtt.Client(client_name)

mqtt_client.connect(server_address, 1883, 60)

############################################

uart = busio.UART(board.TX, board.RX, baudrate=9600, timeout=10)
gps = adafruit_gps.GPS(uart, debug=False)  # Use UART/pyserial
gps.send_command(b"PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0")
gps.send_command(b"PMTK220,1000")
# Main loop runs forever printing the location, etc. every second.
last_print = time.monotonic()

while True:
    # Make sure to call gps.update() every loop iteration and at least twice
    # as fast as data comes from the GPS unit (usually every second).
    # This returns a bool that's true if it parsed new data (you can ignore it
    # though if you don't care and instead look at the has_fix property).
    gps.update()
    # Every second print out current location details if there's a fix.
    current = time.monotonic()
    if current - last_print >= 1.0:
        last_print = current
        if not gps.has_fix:
            # Try again if we don't have a fix yet.
            mqtt_client.publish(topic="gps/status", msg="Waiting for fix...")
            mqtt_client.publish(topic="gps/inuse", msg=str( gps.satellites ))
            continue
        
        # We have a fix! (gps.has_fix is true)
        mqtt_client.publish(topic="gps/status", msg=str(gps.has_fix))
        mqtt_client.publish(topic="gps/inuse", msg=str( gps.satellites ))
        mqtt_client.publish(topic="gps/latitude", msg=str( gps.latitude ))
        mqtt_client.publish(topic="gps/longitude", msg=str( gps.longitude ))
        mqtt_client.publish(topic="gps/altitude", msg=str( gps.altitude_m ))
        
        # Some attributes beyond latitude, longitude and timestamp are optional
        # and might not be present.  Check if they're None before trying to use!
#         if gps.satellites is not None:
#             print("# satellites: {}".format(gps.satellites))
#         if gps.altitude_m is not None:
#             print("Altitude: {} meters".format(gps.altitude_m))
#         if gps.speed_knots is not None:
#             print("Speed: {} knots".format(gps.speed_knots))
#         if gps.track_angle_deg is not None:
#             print("Track angle: {} degrees".format(gps.track_angle_deg))
#         if gps.horizontal_dilution is not None:
#             print("Horizontal dilution: {}".format(gps.horizontal_dilution))
#         if gps.height_geoid is not None:
#             print("Height geoid: {} meters".format(gps.height_geoid))

