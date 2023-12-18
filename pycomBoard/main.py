import time
import socket
from network import WLAN
from Pms7003 import Pms7003 as Pms7003Class

pms_instance = Pms7003Class(1)
host = '192.168.88.214/aqi'  # Replace with your actual API endpoint
api_endpoint = 'http://192.168.88.214:8000/aqi'  # Replace with your actual API endpoint

wlan = WLAN()
wlan.connect(ssid='', auth=(WLAN.WPA2, ''))
print('connecting..',end='')
while not wlan.isconnected():
    time.sleep(1)
    print('.',end='')

while True:
    try:
        sensor_data = pms_instance.read()
        PM1_0 = sensor_data['PM1_0_ATM']
        PM2_5 = sensor_data['PM2_5_ATM']
        PM10_0 = sensor_data['PM10_0_ATM']
        print('PM1.0: {} μg/m³\t PM2.5: {} μg/m³\t PM10: {} μg/m³'.format(PM1_0, PM2_5, PM10_0))

        payload = {
            'pm1_0_concentration': PM1_0,
            'pm2_5_concentration': PM2_5,
            'pm10_concentration': PM10_0
        }

        # Convert data to a string
        # payload_str = json.dumps(payload)

        # Create a socket connection
        s = socket.socket()
        addr = socket.getaddrinfo('192.168.88.214', 8000)[0][-1]
        print(addr)
        s.connect(addr)

        json_payload = '{"pm1_0_concentration": 10.5, "pm2_5_concentration": 20.3, "pm10_concentration": 30.1}'
        content_length = len(json_payload)

        http_request = "POST /aqi HTTP/1.1\r\n" \
                       "Host: 192.168.88.214:8000\r\n" \
                       "Content-Type: application/json\r\n" \
                       "Content-Length: {}\r\n\r\n" \
                       "{}".format(content_length, json_payload)

        s.send(http_request.encode())

        # Receive and print the response
        rec_bytes = s.recv(4096)
        print("Response from server:", rec_bytes.decode())

        # Close the socket
        s.close()
    except Exception as e:
        print("Error:", e)
    time.sleep(5)
