
class mqtt:

    def __init__(self, topic, url, qos=0, retain=False):
        import paho.mqtt.client as mqtt
        import json
        self.topic = topic
        self.url = url
        self.qos = qos
        self.retain = retain

        self.client = mqtt.Client()
        self.client.will_set(
            self.topic, payload=json.dumps({"status": "disconnected"}), qos=self.qos, retain=self.retain)

        # run code until connect
        self.connected = False
        self.printed = False
        while self.connected is False:
            try:
                self.client.connect(url, 1883, 60)
                self.connected = True
            except:
                if self.printed is False:
                    print(
                        "unable to establish connection with topic:'%s', retrying...." % self.topic)
                    self.printed = True

        self.client.publish(self.topic, json.dumps({"status": "connected"}))
        self.client.loop_start()
        print("done topic:'%s' connection setup." % self.topic)

    def send(self, value):
        self.client.publish(self.topic, value, retain=False)
