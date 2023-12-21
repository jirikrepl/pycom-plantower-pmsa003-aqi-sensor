import time
import socket
import ujson
import pycom
from network import WLAN
from Pms7003 import Pms7003 as Pms7003Class
from secrets import WIFI_SSID, WIFI_PASSWORD, HOST, PORT, API_ENDPOINT

pycom.heartbeat(False)  # disable the heartbeat LED

pms_instance = Pms7003Class(1)

wlan = WLAN()
wlan.connect(ssid=WIFI_SSID, auth=(WLAN.WPA2, WIFI_PASSWORD))
print('connecting..', end='')
while not wlan.isconnected():
    time.sleep(1)
    print('.', end='')

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
        json_payload = ujson.dumps(payload)
        content_length = len(json_payload)

        my_socket = socket.socket()
        my_socket.connect((HOST, PORT))

        http_request = "POST {} HTTP/1.1\r\n" \
                       "Host: {}:{}\r\n" \
                       "Content-Type: application/json\r\n" \
                       "Content-Length: {}\r\n\r\n" \
                       "{}".format(API_ENDPOINT, HOST, PORT, content_length, json_payload)
        my_socket.send(http_request.encode())

        # Receive and print the response
        rec_bytes = my_socket.recv(4096)
        print("Response from server:", rec_bytes.decode())

        # Close the socket
        my_socket.close()
    except Exception as e:
        print("Error:", e)
    time.sleep(60)
