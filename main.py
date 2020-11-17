import i2c_arduino_mod as i2c
import time
import unixtime_api as clock


# sensor type 1 fpr ph , 2 for turbidity
while True:
    try:
        value = i2c.read_arduino(11, 1)
        current_time = clock.getnow()
        print("current time: %s" % current_time)
        print("sensor value: %s" % value)
        time.sleep(2)
    except Exception as e:
        print("error occured: ")
        print(e)
        time.sleep(2)
