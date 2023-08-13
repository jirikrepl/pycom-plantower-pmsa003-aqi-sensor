import time
from Pms7003 import Pms7003 as Pms7003Class

pms_instance = Pms7003Class(1)

while True:
    try:
        sensor_data = pms_instance.read()
        PM1_0 = sensor_data['PM1_0']
        PM2_5 = sensor_data['PM2_5']
        PM10_0 = sensor_data['PM10_0']
        print('PM1.0: {} μg/m³\t PM2.5: {} μg/m³\t PM10: {} μg/m³'.format(PM1_0, PM2_5, PM10_0))
    except Exception as e:
        print("Error:", e)
    time.sleep(1)
