import i2c_arduino_mod as i2c
import time
import json
import unixtime_api as clock
from mqtt import mqtt
from config import config

topic = config.topic
mqtt_url = config.mqtt_url
time_url = config.time_url
list_name = config.list_name

ph_mqtt = mqtt(topic, mqtt_url)
# sensor type 1 fpr ph, 2 for turbidity
while True:
    try:
        value = str(i2c.read_arduino(11, 1))
        current_time = str(clock.getnow(time_url, list_name))
        data = {"time": current_time, "value": value}
        ph_mqtt.send(json.dumps(data))
        time.sleep(2)
    except Exception as e:
        print("error occured: ")
        print(e)
        time.sleep(2)
