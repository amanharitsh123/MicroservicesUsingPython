# amqps://drnzmprj:HgGsWmsf5FShF2Zyg4qMcR78nT48Ior1@albatross.rmq.cloudamqp.com/drnzmprj
import pika, json

params = pika.URLParameters('amqp://guest:guest@172.17.0.1:5672/')

connection = pika.BlockingConnection(params)

channel = connection.channel()

def publish(method, body):
    properties = pika.BasicProperties(method)
    channel.basic_publish(exchange='', routing_key='admin', body=json.dumps(body), properties=properties)