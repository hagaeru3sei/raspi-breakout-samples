#!/usr/bin/env python3
import smbus2
from time import sleep


def main():
    bus = smbus2.SMBus(1)
    while True:
        raw_data = bus.read_byte_data(0x48, 0x00)
        data = abs((((raw_data & 0xff00) >> 8 | (raw_data & 0xff) << 8) >> 3) * 0.0625)
        print(data)
        sleep(1)


if __name__ == '__main__':
    main()
