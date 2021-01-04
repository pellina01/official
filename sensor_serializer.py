class serializer:
    from i2c import read_arduino
    from wire1 import read_value
    from do import read_do
    import logging
    import traceback
    import json

    def __formatter(self, value, topic):
        print({"topic": topic, "status": "sending", "value": str(value)})
        return self.json.dumps({"status": "sending", "value": str(value)})

    def __serialize(self, mqtt_send, sensor_function, topic, slave_addr, sensor_type):
        def get_then_send():
            mqtt_send(self.__formatter(
                sensor_function(slave_addr, sensor_type), topic))
        return(get_then_send)

    def __init__(self, url, sensor_parameters):
        from mqtt import mqtt

        self.logging.basicConfig(filename="error.log")

        sensor_type = sensor_parameters[3]
        slave_addr = sensor_parameters[2]
        sensor_function = sensor_parameters[1]
        topic = sensor_parameters[0]
        switch = {
            "read_arduino": read_arduino,
            "read_value": read_value,
            "read_do": read_do
        }
        self.get_send = self.__serialize(
            mqtt(topic, url).send,
            switch.get(sensor_function),
            topic,
            slave_addr,
            sensor_type
        )

    def process(self):
        try:
            self.get_send()
        except Exception as e:
            self.logging.error(self.traceback.format_exc())
            print(e)
