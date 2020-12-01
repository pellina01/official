from i2c_arduino_mod import read_arduino
from unixtime_api import get_time
from mqtt import mqtt
from temp import read_value
import time
import json
import logging
import traceback
import configparser

config = configparser.ConfigParser()
config.read('config.ini')
mqtt_url = config['raspi']['mqtt_url']
time_url = config['raspi']['time_url']
unix_name = config['raspi']['unix_name']
time_url2 = config['raspi']['time_url2']
unix_name2 = config['raspi']['unix_name2']
del config

logging.basicConfig(filename='error.log')

ph_mqtt = mqtt('ph', mqtt_url)
tb_mqtt = mqtt('tb', mqtt_url)
temp_mqtt = mqtt('temp', mqtt_url)
read_time = get_time(time_url, unix_name, time_url2, unix_name2)


def formatter(value):
    return json.dumps({"status": "sending", "time": str(read_time()), "value": str(value)})


while True:
    try:
        ph_mqtt.send(formatter(read_arduino(11, 1)))
        tb_mqtt.send(formatter(read_arduino(11, 2)))
        temp_mqtt.send(formatter(read_value()))
        time.sleep(30)
    except Exception as e:
        print("error occured: %s" % traceback.format_exc())
        print("error message: %s" % e)
        logging.error(traceback.format_exc())
        time.sleep(2)
