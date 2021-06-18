import pika, json, time, sys
from main import Product, db

params = pika.URLParameters('amqp://guest:guest@172.17.0.1:5672/')

connection = pika.BlockingConnection(params)

channel = connection.channel()


channel.queue_declare(queue='main')

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
    print('Recieved in main')
    data = json.loads(body)
    print(data)

    if properties.content_type == 'product_created':
        product = Product(id=data['id'], title=data['title'], image=data['image'])
        db.session.add(product)
        db.session.commit()
    
    elif properties.content_type == 'product_updated':
        product = Product.query.get(data['id'])
        product.title = data['title']
        product.image = data['image']
        db.session.commit()
    
    elif properties.content_type == 'product_deleted':
        product = Product.query.get(data)
        db.session.delete(product)
        db.session.commit()
    
    keep_heartbeat(rabbitmq_channel=ch,total_seconds=30)


channel.basic_consume(queue='main', on_message_callback=callback, auto_ack=True)

print('Started Consuming')

channel.start_consuming()

channel.close()
 