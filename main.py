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
# import pika


def internet_on():
    return os.system("sudo ping -c 1 " + raspi["mqtt_url"]) == 0


def formatter(value, topic, connected):
    if connected:
        print({"topic": topic, "status": "sending", "value": str(value)})
        return json.dumps({"status": "sending", "value": str(value)})
    else:
        print({"topic": topic, "value": str(value),
               "time": str(datetime.datetime.now())})
        return json.dumps({"topic": topic, "value": str(value),
                           "time": str(datetime.datetime.now())})


def sensor_serializer(rabbitmq_insert, mqtt_send, format, sensor_function, topic, *arg):
    def get():
        if internet_on():
            mqtt_send(format(sensor_function(arg[0], arg[1]), topic, True))
        else:
            rabbitmq_insert(
                format(sensor_function(arg[0], arg[1]), topic, False))
    return(get)


if __name__ == "__main__":
    time.sleep(300)
    connected = internet_on()
    is_printed = False
    while not connected:
        time.sleep(3)
        connected = internet_on()
        if is_printed is False:
            print("cant reach the cloud server. retrying.....")
            is_printed = True

    print("cloud server has been reached")

    with open('config.json', 'r') as file:
        data = json.loads(file.read())

    raspi = {}
    for key, value in data["raspi"].items():
        raspi.update({key: value})

    logging.basicConfig(filename=raspi["error_file"])

    rabbit_mq = rabbitmq(raspi["mqtt_url"], "sensor_queue")

    ph_mqtt = mqtt(raspi["ph_topic"], raspi["mqtt_url"])
    tb_mqtt = mqtt(raspi["tb_topic"], raspi["mqtt_url"])
    temp_mqtt = mqtt(raspi["temp_topic"], raspi["mqtt_url"])

    ph_send = sensor_serializer(
        rabbit_mq.insert, ph_mqtt.send, formatter, read_arduino, raspi["ph_topic"], 11, 1)
    tb_send = sensor_serializer(
        rabbit_mq.insert, tb_mqtt.send, formatter, read_arduino, raspi["tb_topic"], 11, 2)
    temp_send = sensor_serializer(
        rabbit_mq.insert, temp_mqtt.send, formatter, read_value, raspi["temp_topic"], 0, 0)

    while True:
        try:
            ph_send()
            tb_send()
            temp_send()
            time.sleep(30)
        except Exception as e:
            logging.error(traceback.format_exc())
            time.sleep(5)
    # # rabbitmq object
    # connection = pika.BlockingConnection(
    #     pika.ConnectionParameters(host=raspi["mqtt_url"]))
    # channel = connection.channel()
    # channel.queue_declare(queue='task_queue', durable=True)

# rabbitmq client
# def rabbit(json_msg):
#     channel.basic_publish(
#         exchange='',
#         routing_key='task_queue',
#         body=json_msg,
#         properties=pika.BasicProperties(
#             delivery_mode=2,  # make message persistent
#         ))
#     print(" [x] Sent to queue %s" % json_msg)
