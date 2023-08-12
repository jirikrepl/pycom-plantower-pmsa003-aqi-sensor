from machine import UART
import time

START_CHARACTER_1 = b'\x42'
START_CHARACTER_2 = b'\x4D'

uart = UART(1, 9600)

def read_sensor_data():
    data = bytearray()
    while True:
        uart_bytes_length = uart.any()
        # print('uart_bytes_lenth:', uart_bytes)
        if uart_bytes_length:
            first_byte = uart.read(1)
            # print('first_byte:', first_byte)
            if first_byte == START_CHARACTER_1:
                data += first_byte
                second_byte = uart.read(1)
                # print('second_byte:', second_byte)
                if second_byte == START_CHARACTER_2:
                    data += second_byte
                    data += uart.read(30)
                    # Clear any remaining bytes in the UART buffer
                    while uart.any():
                        uart.read(1)
                    return data

def extract_pm_concentration(data, low_byte_index, high_byte_index):
    low_byte = data[low_byte_index]
    high_byte = data[high_byte_index]
    pm_concentration = (high_byte << 8) | low_byte
    return pm_concentration / 10.0  # Convert to μg/m³

while True:
    try:
        sensor_data = read_sensor_data()
        # Process sensor_data here
        # print("Sensor data:", sensor_data)
        pm1_concentration = extract_pm_concentration(sensor_data, 4, 5)
        pm25_concentration = extract_pm_concentration(sensor_data, 6, 7)
        pm10_concentration = extract_pm_concentration(sensor_data, 8, 9)
        print("PM1.0:", pm1_concentration, "μg/m³")
        print("PM2.5:", pm25_concentration, "μg/m³")
        print("PM10:", pm10_concentration, "μg/m³")
        print()  # Print a new line
    except Exception as e:
        print("Error:", e)
    time.sleep(1)
