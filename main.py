# import i2c_arduino_mod as i2c
import time
import unixtime_api as clock
from mqtt import mqtt

topic = "topic/ph"
url = "ec2-18-206-177-119.compute-1.amazonaws.com"

ph_mqtt = mqtt(topic, url)

# sensor type 1 fpr ph, 2 for turbidity
while True:
    try:
        value = i2c.read_arduino(11, 1)
        current_time = clock.getnow()
        to_send = str(value) + " at " + str(current_time)
        ph_mqtt.send(current_time)
        time.sleep(2)
    except Exception as e:
        print("error occured: ")
        print(e)
        time.sleep(2)
