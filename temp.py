from w1thermsensor import W1ThermSensor
import time


def read_value():
    sensor = W1ThermSensor()
    temperature_in_celsius = sensor.get_temperature()
    return temperature_in_celsius
