import i2c_arduino_mod as i2c
import time


# sensor type 1 fpr ph , 2 for turbidity
while True:
    try:
        value = i2c.read_arduino(11, 1)
        print(value)
        print("end")
        time.sleep(2)
    except:
        print("error occured")
        time.sleep(2)
