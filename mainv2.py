# edited for actual application
from i2c import read_arduino
from mqtt import mqtt
from wire1 import read_value
import time
import json
import logging
import traceback
import os
import datetime
from do import read_do

with open('configv2.json', 'r') as file:
    data = json.loads(file.read())

raspi = {}
for key, value in data["raspi"].items():
    raspi.update({key: value})


def has_internet():
    return os.system("sudo ping -c 1 " + raspi["mqtt_url"]) == 0


def formatter(value, topic):
    print({"topic": topic, "status": "sending", "value": str(value)})
    return json.dumps({"status": "sending", "value": str(value)})


def sensor_serializer(mqtt_send, format, sensor_function, topic, slave_addr, sensor_type):
    def get_then_send():
        mqtt_send(format(sensor_function(slave_addr, sensor_type), topic, True))
    return(get_then_send)


if __name__ == "__main__":

    is_printed = False

    while not has_internet():
        time.sleep(3)
        if is_printed is False:
            print("cant reach the cloud server. retrying.....")
            is_printed = True

    print("cloud server has been reached")

    logging.basicConfig(filename=raspi["error_file"])

    switch = {
        "i2c": read_arduino,
        "w1_temp": read_value,
        "w1_do": read_do
    }

    sensor_list = []
    for sensor in raspi["sensors"]:
        sensor_list.append(sensor_serializer(
            mqtt(sensor[0], raspi["mqtt_url"]).send,
            formatter, switch.get(sensor[1]), sensor[0], sensor[2], sensor[3]))

    while True:
        try:
            for sensor in sensor_list:
                sensor()
            time.sleep(30)
        except Exception as e:
            logging.error(traceback.format_exc())
            time.sleep(5)
