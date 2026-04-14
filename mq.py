import pika
from environment import ENVIRONMENT
from main import main

def callback(_ch, _method, _properties, body):
    main(body)

def setup_queue():
    environment = ENVIRONMENT()

    queue_url = environment.get('CLOUDAMQP_URL')
    params = pika.URLParameters(queue_url)
    connection = pika.BlockingConnection(params)
    channel = connection.channel() # start a channel
    channel.queue_declare(queue='date_collected') # Declare a queue

    channel.basic_consume(
        'date_collected', 
        callback, 
        auto_ack=True,
        inactivity_timeout=(3600 * 72)) #three days with now messages closes the connection

    channel.start_consuming()
    channel.close()