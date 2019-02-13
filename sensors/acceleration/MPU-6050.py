#!/usr/bin/env python3
import threading
import time
import smbus2
import numpy as np
import matplotlib.pyplot as plt


class MPU_6050:

    bus = None
    sensor_address = 0x68
    x_history = []
    y_history = []
    z_history = []

    def __init__(self):
        try:
            self.bus = smbus2.SMBus(1)
        except FileNotFoundError:
            raise FileNotFoundError("Acceleration sensor is not found.")
        self.bus.write_byte_data(self.sensor_address, 0x6b, 0x00)

    def read(self, address):
        high = self.bus.read_byte_data(self.sensor_address, address)
        low = self.bus.read_byte_data(self.sensor_address, address + 1)
        value = (high << 8) + low
        if (value >= 0x8000):
            return -((65535 - value) + 1)
        else:
            return value
 
    def detect(self) -> tuple:
        x = '{:+.10f}'.format(self.read(0x3b) / 16384.0)
        y = '{:+.10f}'.format(self.read(0x3d) / 16384.0)
        z = '{:+.10f}'.format(self.read(0x3f) / 16384.0)
        #print('x:{:+.10f}, y:{:+.10f}, z:{:+.10f}'.format(x, y, z))
        #raw_data = self.bus.read_byte_data(self.sensor_address, 0x1c)
        return x, y, x,


def main():

    acc = MPU_6050()

    while True:
        x, y, z = acc.detect()

        acc.x_history.append(float(x))
        acc.y_history.append(float(y))
        acc.z_history.append(float(z))
        if len(acc.x_history) == 1000:
            fig, ax = plt.subplots()
            ax.set(xlabel='time', ylabel='value')
            ax.set_ylim(-2, 2)
            ax.grid(True)

            s = np.array(acc.x_history)
            ax.plot(s)

            s = np.array(acc.y_history)
            ax.plot(s)

            s = np.array(acc.z_history)
            ax.plot(s)

            fig.savefig('acc.png')

            acc.x_history.clear()
            acc.y_history.clear()
            acc.z_history.clear()

            plt.close()

        #print('{},{},{}'.format(z, y, z))
        time.sleep(.01)
  

if __name__ == "__main__":
    main()

