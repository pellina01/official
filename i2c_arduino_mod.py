import smbus2 as smbus

# sensor type 1 fpr ph , 2 for turbidity


# def convert_strings_to_bytes(src):
#     converted = bytes(src, "utf-8")
#     convert = []
#     for byte in converted:
#         convert.append(byte)
#     return convert
# hello

def read_arduino(slave_addr, sensor_type):
    I2Cbus = smbus.SMBus(1)
    i2c_slave_address = slave_addr
    # byte = convert_strings_to_bytes(sensor_type)
    I2Cbus.write_i2c_block_data(i2c_slave_address, 0x00, sensor_type)
    response = I2Cbus.read_i2c_block_data(i2c_slave_address, 0x00, 5)
    return(response)
