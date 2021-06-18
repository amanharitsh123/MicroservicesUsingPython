import pika, json, os, django, time, sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "admin.settings")
django.setup()

from products.models import Product

params = pika.URLParameters('amqp://guest:guest@172.17.0.1:5672/')

connection = pika.BlockingConnection(params)

channel = connection.channel()


channel.queue_declare(queue='admin') 

def keep_heartbeat(rabbitmq_channel, total_seconds, dot_seconds=10, line_seconds=100):
    connection = rabbitmq_channel._connection

    for i in range(total_seconds):
        if (i+1) % dot_seconds == 0:
            sys.stdout.write('.')
        if (i+1) % line_seconds == 0:
            sys.stdout.write('\n')
        if (i+1) % 30 == 0:
            connection.process_data_events()
        time.sleep(1)


def callback(ch, method, properties, body):
    print('Recieved in admin')
    id = json.loads(body)
    print(id)
    product = Product.objects.get(id=id)
    product.likes = product.likes + 1
    product.save()
    print('Product likes increased')
    keep_heartbeat(rabbitmq_channel=ch,total_seconds=30)

channel.basic_consume(queue='admin', on_message_callback=callback, auto_ack=True)

print('Started Consuming')

channel.start_consuming()

channel.close()
 