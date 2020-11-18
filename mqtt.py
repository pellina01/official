import paho.mqtt.client as mqtt


client = mqtt.Client()
client.will_set("topic/test1", payload="Connection lost", qos=0, retain=False)
client.connect("ec2-3-236-14-224.compute-1.amazonaws.com", 1883, 60)
client.publish("topic/test1", "CONNECTION OK")

client.loop_start()


def send(value):
    client.publish("topic/test1", value, retain=False)
