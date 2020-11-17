import i2c_arduino_mod as i2c

value = i2c.read_arduino(1, "ph")
print(value)
