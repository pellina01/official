import smbus2 as smbus

# sensor type 1 for ph , 2 for turbidity


def convert_bytes_to_list(src):
    convert = []
    for byte in src:
        convert.append(byte)
    return convert


def read_arduino(slave_addr, sensor_type):
    try:
        I2Cbus = smbus.SMBus(1)
        byte = convert_bytes_to_list(bytes(str(sensor_type), "utf-8"))
        I2Cbus.write_i2c_block_data(slave_addr, 0x00, byte)
        response = I2Cbus.read_i2c_block_data(slave_addr, 0x00, 25)
        res = bytearray(response).decode("utf-8", "ignore")
        del I2Cbus
        del byte
        del response
        return(float(res))
    except:
        print("failed to retrieve data from arduino...")
