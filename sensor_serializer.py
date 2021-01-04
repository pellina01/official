class serializer:
    from i2c import read_arduino
    from wire1 import read_value
    from do import read_do
    import logging
    import traceback

    def __formatter(self, value, topic):
        print({"topic": topic, "status": "sending", "value": str(value)})
        return self.json.dumps({"status": "sending", "value": str(value)})

    def __init__(self, url, sensor):
        import json
        from mqtt import mqtt

        self.logging.basicConfig(filename="error.log")
        self.json = json

        sensor_type = sensor[3]
        slave_addr = sensor[2]
        sensor_function = sensor[1]
        topic = sensor[0]
        switch = {
            "read_arduino": read_arduino,
            "read_value": read_value,
            "read_do": read_do
        }
        self.get_send = mqtt(topic, url).send(
            self.__formatter(
                switch.get(sensor_function)(slave_addr, sensor_type),
                topic
            )
        )

    def process(self):
        try:
            self.get_send()
        except Exception as e:
            self.logging.error(traceback.format_exc())
            print(e)
