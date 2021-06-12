import pika

params = pika.URLParameters('amqp://guest:guest@34.134.210.216:5672/')

connection = pika.BlockingConnection(params)

channel = connection.channel()


channel.queue_declare(queue='main')

def callback(ch, method, properties, body):
    print('Recieved in admin')
    print(body)

channel.basic_consume(queue='main', on_message_callback=callback, auto_ack=True)

print('Started Consuming')

channel.start_consuming()

channel.close()
 