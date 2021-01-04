import json
import logging
import traceback
from sensor_serializer import sensor as sensor_object
from check_internet import check as internet_check
from multiprocessing import Process
from executor import executor


def main():
    with open('configv2.json', 'r') as file:
        data = json.loads(file.read())

    raspi = {}
    for key, value in data["raspi"].items():
        raspi.update({key: value})

    internet_check(raspi["mqtt_url"])

    logging.basicConfig(filename="error.log")

    sensor_list = []
    for listed_sensor in raspi["sensors"]:
        sensor_list.append(
            executor(
                sensor_object(raspi["mqtt_url"], listed_sensor).process,
                raspi["frequency"]
            )
        )

    processes = []
    try:
        for sensor in sensor_list:
            process = Process(target=sensor.execute)
            process.start()
            processes.append(process)
        for process in processes:
            process.join()
            processes.remove(process)
    except Exception as e:
        logging.error(traceback.format_exc())


if __name__ == "__main__":
    main()
