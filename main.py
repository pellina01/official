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

del config

ph_mqtt = mqtt(ph, mqtt_url)
tb_mqtt = mqtt(tb, mqtt_url)
temp_mqtt = mqtt(temp, mqtt_url)

sensor_info = {
    "ph_value": "",
    "tb_value": "",
    "temp_value": "",
    "current_time": ""
}

data = {
    "ph": "",
    "tb": "",
    "temp": ""
}


while True:
    try:
        # sensor type 1 for ph, 11 for arduino i2c address
        sensor_info['ph_value'] = str(i2c.read_arduino(11, 1))
        # sensor type 2 for turbidity, 11 for arduino i2c address
        sensor_info['tb_value'] = str(i2c.read_arduino(11, 2))
        sensor_info['temp_value'] = str(w1temp.read_value())

        sensor_info['current_time'] = str(clock.getnow(
            time_url, unix_name, time_url2, unix_name2))

        data["ph"] = {"status": "sending",
                      "time": sensor_info['current_time'], "value": sensor_info['ph_value']}
        data["tb"] = {"status": "sending",
                      "time": sensor_info['current_time'], "value": sensor_info['tb_value']}
        data["temp"] = {"status": "sending",
                        "time": sensor_info['current_time'], "value": sensor_info['temp_value']}
        ph_mqtt.send(json.dumps(data["ph"]))
        tb_mqtt.send(json.dumps(data["ph"]))
        temp_mqtt.send(json.dumps(data["ph"]))
        time.sleep(30)
    except Exception as e:
        print("error occured: %s" % traceback.format_exc())
        print("error message: %s" % e)
        logging.error(traceback.format_exc())
        time.sleep(2)
