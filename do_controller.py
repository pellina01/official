from temp import read_value
import mqtt as mqtt
import time

temp = 30

aerator_mqtt = mqtt("aerator", "localhost")

while temp > 29:
    temp = read_value()
    if temp > 29:
        aerator_mqtt.send("on")
        time.sleep(10)
    else:
        aerator_mqtt.send("off")
