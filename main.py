import i2c_arduino_mod as i2c
import unixtime_api as clock
from mqtt import mqtt
from config_raspi import config
import temp as w1temp
import time
import json
import traceback
#import datetime


import logging


error = config.error_file
mqtt_url = config.mqtt_url
time_url = config.time_url
unix_name = config.unix_name


logging.basicConfig(filename=error)

ph = config.ph_topic
tb = config.tb_topic
temp = config.temp_topic

ph_mqtt = mqtt(ph, mqtt_url)
tb_mqtt = mqtt(tb, mqtt_url)
temp_mqtt = mqtt(temp, mqtt_url)

# sensor type 1 fpr ph, 2 for turbidity
while True:
    try:
        ph_value = str(i2c.read_arduino(11, 1))
        tb_value = str(i2c.read_arduino(11, 2))
        temp_value = str(w1temp.read_value())

        current_time = str(clock.getnow(time_url, unix_name))
        ph_data = {"status": "sending",
                   "time": current_time, "value": ph_value}
        tb_data = {"status": "sending",
                   "time": current_time, "value": tb_value}
        temp_data = {"status": "sending",
                     "time": current_time, "value": temp_value}
        ph_mqtt.send(json.dumps(ph_data))
        tb_mqtt.send(json.dumps(tb_data))
        temp_mqtt.send(json.dumps(temp_data))
        time.sleep(2)
    except Exception as e:
        print("error occured: " + traceback.format_exc())
        print("error message: " + e)
        logging.error(traceback.format_exc())
        time.sleep(2)
