# edited for actual application
from i2c_arduino_mod import read_arduino
from mqtt import mqtt
from rabbit import rabbitmq
from temp import read_value
import time
import json
import logging
import traceback
import os
import datetime
from do import read_do

time.sleep(5)

with open('config.json', 'r') as file:
    data = json.loads(file.read())

raspi = {}
for key, value in data["raspi"].items():
    raspi.update({key: value})

CLOUD_SERVER = raspi["mqtt_url"]
ADDR_SLAVE = 11
TYPE_PH = 1
TYPE_TB = 2
PLACE_HOLDER = 0
LOCAL_HOST = "127.0.0.1"


def has_internet():
    return os.system("sudo ping -c 1 " + CLOUD_SERVER) == 0


# def formatter(value, topic, is_connected):
#     if is_connected:
#         print({"topic": topic, "status": "sending", "value": str(value)})
#         return json.dumps({"status": "sending", "value": str(value)})
#     else:
#         print({"topic": topic, "value": str(value),
#                "time": str(datetime.datetime.now())})
#         return json.dumps({"topic": topic, "value": str(value),
#                            "time": str(datetime.datetime.now())})


# def sensor_serializer(rabbitmq_insert, mqtt_send, format, sensor_function, topic, slave_addr, sensor_type):
#     def get_then_send():
#         if has_internet():
#             mqtt_send(format(sensor_function(slave_addr, sensor_type), topic, True))
#         else:
#             rabbitmq_insert(
#                 format(sensor_function(slave_addr, sensor_type), topic, False))
#     return(get_then_send)

def formatter(value, topic, is_connected):
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

    # rabbit_mq = rabbitmq(LOCAL_HOST, "sensor_queue")

    ph_mqtt = mqtt(raspi["ph_topic"], CLOUD_SERVER)
    tb_mqtt = mqtt(raspi["tb_topic"], CLOUD_SERVER)
    temp_mqtt = mqtt(raspi["temp_topic"], CLOUD_SERVER)
    do_mqtt = mqtt(raspi["do_topic"], CLOUD_SERVER)

    # ph_send = sensor_serializer(
    #     rabbit_mq.insert, ph_mqtt.send, formatter, read_arduino, raspi["ph_topic"], ADDR_SLAVE, TYPE_PH)
    # tb_send = sensor_serializer(
    #     rabbit_mq.insert, tb_mqtt.send, formatter, read_arduino, raspi["tb_topic"], ADDR_SLAVE, TYPE_TB)
    # temp_send = sensor_serializer(
    #     rabbit_mq.insert, temp_mqtt.send, formatter, read_value, raspi["temp_topic"], PLACE_HOLDER, PLACE_HOLDER)
    # do_send = sensor_serializer(
    #     rabbit_mq.insert, do_mqtt.send, formatter, read_do, raspi["do_topic", PLACE_HOLDER, PLACE_HOLDER)

    ph_send = sensor_serializer(
        ph_mqtt.send, formatter, read_arduino, raspi["ph_topic"], ADDR_SLAVE, TYPE_PH)
    tb_send = sensor_serializer(
        tb_mqtt.send, formatter, read_arduino, raspi["tb_topic"], ADDR_SLAVE, TYPE_TB)
    temp_send = sensor_serializer(
        temp_mqtt.send, formatter, read_value, raspi["temp_topic"], PLACE_HOLDER, PLACE_HOLDER)
    do_send = sensor_serializer(
        do_mqtt.send, formatter, read_do, raspi["do_topic", PLACE_HOLDER, PLACE_HOLDER)

    while True:
        try:
            ph_send()
            tb_send()
            temp_send()
            do_send()
            time.sleep(30)
        except Exception as e:
            logging.error(traceback.format_exc())
            time.sleep(5)
