from i2c_arduino_mod import read_arduino
# from unixtime_api import get_time
from mqtt import mqtt
from temp import read_value
import time
import json
import logging
import traceback
# json_file = open('config.json')
# data = json.load(json_file)
# json_file.close()

with open('config.json', 'r') as file:
    data = json.loads(file.read())

raspi = {}
for key, value in data["raspi"].items():
    raspi.update({key: value})

logging.basicConfig(filename=raspi["error_file"])

ph_mqtt = mqtt(raspi["ph_topic"], raspi["mqtt_url"])
tb_mqtt = mqtt(raspi["tb_topic"], raspi["mqtt_url"])
temp_mqtt = mqtt(raspi["temp_topic"], raspi["mqtt_url"])
# read_time = get_time(raspi["time_url"], raspi["unix_name"],
#                      raspi["time_url2"], raspi["unix_name2"])


def formatter(value, topic):
    print({"topic": topic, "status": "sending", "value": str(value)})
    return json.dumps({"status": "sending", "value": str(value)})


while True:
    try:
        ph_mqtt.send(formatter(read_arduino(11, 1), "ph"))
        tb_mqtt.send(formatter(read_arduino(11, 2), "tb"))
        temp_mqtt.send(formatter(read_value(), "temp"))
        time.sleep(30)
    except Exception as e:
        print("error occured: %s" % traceback.format_exc())
        print("error message: %s" % e)
        logging.error(traceback.format_exc())
        time.sleep(2)
