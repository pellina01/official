from w1thermsensor import W1ThermSensor
import time


def read_value(*args):
    sensor = W1ThermSensor()
    temperature_in_celsius = sensor.get_temperature()
    del sensor
    return temperature_in_celsius


if __name__ == "__main__":
    print(read_value())
