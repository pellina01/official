import i2c_arduino_mod as i2c
import time
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
        value = i2c.read_arduino(11, 1)
        current_time = clock.getnow(time_url, list_name)
        to_send = str(value) + " at " + str(current_time)
        ph_mqtt.send(to_send)
        time.sleep(2)
    except Exception as e:
        print("error occured: ")
        print(e)
        time.sleep(2)
