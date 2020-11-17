import i2c_arduino_mod as i2c


# sensor type 1 fpr ph , 2 for turbidity
value = i2c.read_arduino(11, 1)
print(value)
