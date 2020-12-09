# working code for turbidity

from i2c_arduino_mod import read_arduino
from mqtt import mqtt
import time
import json
import logging
import traceback

with open('config.json', 'r') as file:
    data = json.loads(file.read())

raspi = {}
for key, value in data["raspi"].items():
    raspi.update({key: value})

logging.basicConfig(filename=raspi["error_file"])

tb_mqtt = mqtt(raspi["tb_topic"], raspi["mqtt_url"])


def formatter(value, topic):
    print({"topic": topic, "status": "sending", "value": str(value)})
    return json.dumps({"status": "sending", "value": str(value)})


while True:
    try:
        tb_mqtt.send(formatter(read_arduino(11, 2), "tb"))
        time.sleep(30)
    except Exception as e:
        print("error occured: %s" % traceback.format_exc())
        print("error message: %s" % e)
        logging.error(traceback.format_exc())
        time.sleep(2)
