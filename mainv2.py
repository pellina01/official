import time
import json
import logging
import traceback
from sensor_serializer import serializer
from check_internet import check
from multiprocessing import Process


def main():
    with open('configv2.json', 'r') as file:
        data = json.loads(file.read())

    raspi = {}
    for key, value in data["raspi"].items():
        raspi.update({key: value})

    check(raspi["mqtt_url"])

    logging.basicConfig(filename="error.log")

    sensor_list = []
    for sensor in raspi["sensors"]:
        sensor_list.append(serializer(raspi["mqtt_url"].send, sensor))

    processes = []
    while True:
        try:
            for sensor in sensor_list:
                process = Process(target=sensor.process)
                process.start()
                processes.append(process)
            for process in processes:
                process.join()
                processes.remove(process)
            time.sleep(30)
        except Exception as e:
            logging.error(traceback.format_exc())
            time.sleep(5)


if __name__ == "__main__":
    main()
