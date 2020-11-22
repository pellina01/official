
class mqtt:

    def __init__(self, topic, url):
        import paho.mqtt.client as mqtt
        import json
        import time
        self.connected = False
        self.topic = topic
        self.client = mqtt.Client()
        self.client.will_set(
            self.topic, payload=json.dumps({"status": "disconnected"}), qos=0, retain=False)

        # run code until connect
        self.printed = False
        while self.connected is False:
            try:
                self.client.connect(url, 1883, 60)
                self.connected = True
            except:
                if self.printed is False:
                    print("failed to connect to %s, retrying...." % url)
                    self.printed = True

        self.client.publish(self.topic, json.dumps({"status": "connected"}))
        self.client.loop_start()
        print("done '%s' mqtt setup" % self.topic)

    def send(self, value):
        self.client.publish(self.topic, value, retain=False)
