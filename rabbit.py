class rabbitmq:

    def __init__(self, host, queue):
        import pika
        import logging
        import traceback
        self.printed = self.connected = False
        self.queue = queue
        self.pika = pika
        while not self.connected:
            try:
                self.connection = pika.BlockingConnection(
                    pika.ConnectionParameters(host))
                self.channel = self.connection.channel()
                self.channel.queue_declare(queue, durable=True)
                self.connected = True
            except:
                if not self.printed:
                    print("failed to connect to rabbitmq server. retrying...")
                    self.printed = True
        # for error logging
        self.logging = logging
        self.traceback = traceback
        self.logging.basicConfig(filename="error.log")

    def insert(self, json_msg):
        try:
            self.channel.basic_publish(
                exchange='',
                routing_key=self.queue,
                body=json_msg,
                properties=self.pika.BasicProperties(delivery_mode=2,))  # make message persistent
            print(" [x] Sent message: %s to queue" % json_msg)
        except:
            print("failed to insert data to queue...")
            self.logging.error(self.traceback.format_exc())
