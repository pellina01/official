import paho.mqtt.client as mqtt


# "topic/test",
class mqtt:

    def __init__(self, topic, url):
        self.topic = topic
        self.client = mqtt.Client()
        client.will_set(
            self.topic, payload="Connection lost", qos=0, retain=False)
        client.connect(url, 1883, 60)
        client.publish(self.topic, "CONNECTION OK")
        client.loop_start()

    def send(self, value):
        client.publish(self.topic, value, retain=False)
