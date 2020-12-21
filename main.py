# edited for actual application

from i2c_arduino_mod import read_arduino
from mqtt import mqtt
from temp import read_value
import time
import json
import logging
import traceback
import pika
import os
import datetime


def internet_on():
    if os.system("sudo ping -c 1 " + raspi["mqtt_url"]) == 0:
        return True
    else:
        return False


def formatter(value, topic, conn):
    if conn:
        print({"topic": topic, "status": "sending", "value": str(value)})
        return json.dumps({"status": "sending", "value": str(value)})
    else:
        print({"topic": topic, "value": str(value),
               "time": str(datetime.datetime.now())})
        return json.dumps({"topic": topic, "value": str(value),
                           "time": str(datetime.datetime.now())})


def sensor_serializer(f1, f2, f3, topic, *arg):
    def get():
        try:
            data = f3(arg[0], arg[1])
            if internet_on():
                f1(f2(data, topic, True))
            else:
                rabbit(f2(data, topic, False))
        except Exception:
            print('error occured: %s at topic %d' %
                  (traceback.format_exc(), topic))
            logging.error(traceback.format_exc())
        finally:
            del data
    return(get)


# rabbitmq client
def rabbit(json_msg):
    channel.basic_publish(
        exchange='',
        routing_key='task_queue',
        body=json_msg,
        properties=pika.BasicProperties(
            delivery_mode=2,  # make message persistent
        ))
    print(" [x] Sent to queue %s" % json_msg)


if __name__ == "__main__":
    time.sleep(300)
    conn = internet_on()
    is_printed = False
    while conn is False:
        conn = internet_on()
        if is_printed is False:
            print("cant reach the cloud server. retrying.....")
            is_printed = True
        time.sleep(3)

    del is_printed
    del conn
    print("cloud server has been reached")

    with open('config.json', 'r') as file:
        data = json.loads(file.read())

    raspi = {}
    for key, value in data["raspi"].items():
        raspi.update({key: value})

    logging.basicConfig(filename=raspi["error_file"])

    ph_mqtt = mqtt(raspi["ph_topic"], raspi["mqtt_url"])
    tb_mqtt = mqtt(raspi["tb_topic"], raspi["mqtt_url"])
    temp_mqtt = mqtt(raspi["temp_topic"], raspi["mqtt_url"])

    # rabbitmq object
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=raspi["mqtt_url"]))
    channel = connection.channel()
    channel.queue_declare(queue='task_queue', durable=True)

    ph_send = sensor_serializer(
        ph_mqtt.send, formatter, read_arduino, "ph", 11, 1)
    tb_send = sensor_serializer(
        tb_mqtt.send, formatter, read_arduino, "tb", 11, 2)
    temp_send = sensor_serializer(temp_mqtt.send, formatter,
                                  read_value, "temp", 0, 0)
    while True:
        ph_send()
        tb_send()
        temp_send()
        time.sleep(30)
