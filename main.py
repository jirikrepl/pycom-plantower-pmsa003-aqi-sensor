from machine import UART
import time

START_CHARACTER_1 = b'\x42'
START_CHARACTER_2 = b'\x4D'

uart = UART(1, 9600)

def read_sensor_data():
    data = bytearray()
    while True:
        if uart.any():
            byte = uart.read(1)
            if byte == START_CHARACTER_1:
                data += byte
                if uart.read(1) == START_CHARACTER_2:
                    data += byte
                    data += uart.read(30)
                    return data

while True:
    try:
        sensor_data = read_sensor_data()
        # Process sensor_data here
        print("Received data:", sensor_data)
        time.sleep(1)
    except Exception as e:
        print("Error:", e)
        time.sleep(5)
