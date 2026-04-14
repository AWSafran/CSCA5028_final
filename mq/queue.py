import pika
from environment import ENVIRONMENT

def send_date_to_queue(date_string):
    environment = ENVIRONMENT()

    queue_url = environment.get('CLOUDAMQP_URL')

    params = pika.URLParameters(queue_url)
    connection = pika.BlockingConnection(params)
    channel = connection.channel() # start a channel
    channel.queue_declare(queue='date_collected') # Declare a queue
    channel.basic_publish(exchange='',
                        routing_key='date_collected',
                        body=date_string)
    
    connection.close()