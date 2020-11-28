import i2c_arduino_mod as i2c
import unixtime_api as clock
from mqtt import mqtt
import temp as w1temp
import time
import json


import logging
import traceback
import configparser


config = configparser.ConfigParser()
config.read('config.ini')


error = config['raspi']['error_file']
mqtt_url = config['raspi']['mqtt_url']
time_url = config['raspi']['time_url']
unix_name = config['raspi']['unix_name']
time_url2 = config['raspi']['time_url2']
unix_name2 = config['raspi']['unix_name2']


logging.basicConfig(filename=error)

ph = config.ph_topic
tb = config.tb_topic
temp = config.temp_topic


ph_mqtt = mqtt(ph, mqtt_url)
tb_mqtt = mqtt(tb, mqtt_url)
temp_mqtt = mqtt(temp, mqtt_url)
connected = True


while True:
    try:
        # sensor type 1 for ph, 11 for arduino i2c address
        ph_value = str(i2c.read_arduino(11, 1))
        # sensor type 2 for turbidity, 11 for arduino i2c address
        tb_value = str(i2c.read_arduino(11, 2))
        temp_value = str(w1temp.read_value())

        current_time = str(clock.getnow(
            time_url, unix_name, time_url2, unix_name2))
        #current_time = int(time.time())

        ph_data = {"status": "sending",
                   "time": current_time, "value": ph_value}
        tb_data = {"status": "sending",
                   "time": current_time, "value": tb_value}
        temp_data = {"status": "sending",
                     "time": current_time, "value": temp_value}
        ph_mqtt.send(json.dumps(ph_data))
        tb_mqtt.send(json.dumps(tb_data))
        temp_mqtt.send(json.dumps(temp_data))
        time.sleep(30)
    except Exception as e:
        print("error occured: %s" % traceback.format_exc())
        print("error message: %s" % e)
        logging.error(traceback.format_exc())
        time.sleep(2)
