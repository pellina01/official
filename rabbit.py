class rabbitmq:
	def __init__(self, host, queue):
		import pika
		printed = connected = False
		self.queue = queue
		while not connected:
			try:
			    self.connection = pika.BlockingConnection(
			        pika.ConnectionParameters(host=host))
			    self.channel = self.connection.channel()
			    self.channel.queue_declare(queue=queue, durable=True)
			    connected = True
			except:
				if not printed:
					print("failed to connect to rabbitmq server. retrying...")
					printed = True
		del printed
		del printed

	def insert(json_msg):
		try:
		    self.channel.basic_publish(
		        exchange='',
		        routing_key=self.queue,
		        body=json_msg,
		        properties=pika.BasicProperties(
		            delivery_mode=2,  # make message persistent
		        ))
		    print(" [x] Sent to queue %s" % json_msg)
		except: 
			print("failed to insert data to queue...")
