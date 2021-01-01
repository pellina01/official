import smbus2 as smbus

# sensor type 1 for ph , 2 for turbidity
MEMORY_ADDR = 0x00
BYTE_LEN = 25
BUS = 1


def convert_bytes_to_list(src):
    convert = []
    for byte in src:
        convert.append(byte)
    return convert


def read_arduino(slave_addr, sensor_type):
    try:
        I2Cbus = smbus.SMBus(BUS)
        byte = convert_bytes_to_list(bytes(str(sensor_type), "utf-8"))
        I2Cbus.write_i2c_block_data(slave_addr, MEMORY_ADDR, byte)
        response = I2Cbus.read_i2c_block_data(
            slave_addr, MEMORY_ADDR, BYTE_LEN)
        return float(bytearray(response).decode("utf-8", "ignore"))
    except:
        print("failed to retrieve data from arduino...")


if __name__ == "__main__":
    print(read_arduino(11, 1))
    print(read_arduino(11, 2))
