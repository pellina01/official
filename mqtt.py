
class mqtt:

    def __init__(self, topic, url):
        import paho.mqtt.client as mqtt
        self.topic = topic
        self.client = mqtt.Client()
        self.client.will_set(
            self.topic, payload="Connection lost", qos=0, retain=False)
        self.client.connect(url, 1883, 60)
        self.client.publish(self.topic, "CONNECTION OK")
        self.client.loop_start()
        print("done %s mqtt setup" % self.topic)

    def send(self, value):
        self.client.publish(self.topic, value, retain=False)
