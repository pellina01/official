# edited for actual application

from i2c_arduino_mod import read_arduino
from mqtt import mqtt
from temp import read_value
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

ph_mqtt = mqtt(raspi["ph_topic"], raspi["mqtt_url"])
tb_mqtt = mqtt(raspi["tb_topic"], raspi["mqtt_url"])
temp_mqtt = mqtt(raspi["temp_topic"], raspi["mqtt_url"])


def formatter(value, topic):
    print({"topic": topic, "status": "sending", "value": str(value)})
    return json.dumps({"status": "sending", "value": str(value)})

def mqtt_sensor(f1 , f2, f3, topic, *arg):
    def get():
        try:
            f1(f2(f3(arg[0],arg[1]),topic))
        except Exception:
            print("error occured: %s" % traceback.format_exc())
            print("error at topic: %s" % topic)
            logging.error(traceback.format_exc())
            time.sleep(2)
    return(get)

ph_send = mqtt_sensor(ph_mqtt.send, formatter, read_arduino,"ph", 11, 1)
tb_send = mqtt_sensor(tb_mqtt.send, formatter, read_arduino,"tb", 11, 2)
temp_send = mqtt_sensor(temp_mqtt.send, formatter, read_value,"temp", 0, 0)

while True:
    ph_send()
    tb_send()
    temp_send()
    time.sleep(30)

# while True:
#     try:
#         ph_mqtt.send(formatter(read_arduino(11, 1), "ph"))
#         tb_mqtt.send(formatter(read_arduino(11, 2), "tb"))
#         temp_mqtt.send(formatter(read_value(), "temp"))
#         time.sleep(30)
#     except Exception as e:
#         print("error occured: %s" % traceback.format_exc())
#         print("error message: %s" % e)
#         logging.error(traceback.format_exc())
#         time.sleep(2)



