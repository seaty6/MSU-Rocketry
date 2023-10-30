import machine
import time

class accel():
    def __init__(self, i2c, addr=0x68):
        self.iic = i2c
        self.addr = addr
        self.iic.start()
        self.iic.writeto(self.addr, bytearray([107, 0]))
        self.iic.stop()

    def get_raw_values(self):
        self.iic.start()
        a = self.iic.readfrom_mem(self.addr, 0x3B, 14)
        self.iic.stop()
        return a

    def get_ints(self):
        b = self.get_raw_values()
        c = []
        for i in b:
            c.append(i)
        return c

    def bytes_toint(self, firstbyte, secondbyte):
        if not firstbyte & 0x80:
            return firstbyte << 8 | secondbyte
        return - (((firstbyte ^ 255) << 8) | (secondbyte ^ 255) + 1)

    def get_values(self):
        raw_ints = self.get_raw_values()
        vals = {}
        vals["AcX"] = self.bytes_toint(raw_ints[0], raw_ints[1])
        vals["AcY"] = self.bytes_toint(raw_ints[2], raw_ints[3])
        vals["AcZ"] = self.bytes_toint(raw_ints[4], raw_ints[5])
        vals["Tmp"] = self.bytes_toint(raw_ints[6], raw_ints[7]) / 340.00 + 36.53
        vals["GyX"] = self.bytes_toint(raw_ints[8], raw_ints[9])
        vals["GyY"] = self.bytes_toint(raw_ints[10], raw_ints[11])
        vals["GyZ"] = self.bytes_toint(raw_ints[12], raw_ints[13])
        return vals  # returned in range of Int16
        # -32768 to 32767

    def val_test(self):  # ONLY FOR TESTING! Also, fast reading sometimes crashes IIC
        from time import sleep
        while 1:
            print(self.get_values())
            sleep(0.05)
    
    def set_accel_offsets(self, values, offsets):
        values["AcX"] -= offsets[0]
        values["AcY"] -= offsets[1]
        values["AcZ"] -= offsets[2]

        # values[AcX] = 12345
        
        return values
        
    def calibrate(self, dic):
        print("Collecting data for calibration...")
        total_samples = 15
        acc_offsets = [0, 0, 0]

        for _ in range(total_samples):
            # Read raw accelerometer and gyro data
            accel_data = self.get_values()

            # Accumulate offsets
            acc_offsets[0] += accel_data['AcX']
            acc_offsets[1] += accel_data['AcY']
            acc_offsets[2] += accel_data['AcZ']

            time.sleep(0.01)  # Delay for stable readings

        # Calculate average offsets
        acc_offsets = [offset / total_samples for offset in acc_offsets]
        print(acc_offsets)

        # Apply offsets to the sensor
        self.set_accel_offsets(dic, acc_offsets)

        print(f"Accel Offsets: {acc_offsets}")
        
        return acc_offsets
        
            
#i2c = machine.I2C(1, sda=machine.Pin(21), scl=machine.Pin(22))

#accelerate = accel(i2c)

# test_vals = accelerate.get_values()

#print(test_vals["AcX"])