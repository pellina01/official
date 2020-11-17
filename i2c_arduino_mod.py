import smbus2 as smbus

# sensor type 1 for ph , 2 for turbidity


def convert_bytes_to_list(src):
    convert = []
    for byte in src:
        convert.append(byte)
    return convert


def read_arduino(slave_addr, sensor_type):
    I2Cbus = smbus.SMBus(1)
    i2c_slave_address = slave_addr
    byte = convert_bytes_to_list(bytes(str(sensor_type), "utf-8"))
    I2Cbus.write_i2c_block_data(i2c_slave_address, 0x00, byte)
    response = I2Cbus.read_i2c_block_data(i2c_slave_address, 0x00, 5)
    res = bytearray(response).decode("utf-8", "ignore")
    return(res)
