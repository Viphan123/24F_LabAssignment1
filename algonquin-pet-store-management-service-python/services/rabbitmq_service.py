# Service to interact with RabbitMQ
# services/rabbitmq_service.py
import pika
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

RABBITMQ_URL = os.getenv("RABBITMQ_URL")

# Connect to RabbitMQ and create a channel
def connect_to_rabbitmq():
    try:
        connection = pika.BlockingConnection(pika.URLParameters(RABBITMQ_URL))
        channel = connection.channel()
        return connection, channel
    except Exception as e:
        print(f"Error connecting to RabbitMQ: {e}")
        return None, None

# Consume messages from the 'orders_queue'
def consume_orders(callback):
    connection, channel = connect_to_rabbitmq()
    if not channel:
        return

    channel.queue_declare(queue='orders_queue', durable=True)

    def on_message(ch, method, properties, body):
        print(f"Received order: {body}")
        callback(body.decode("utf-8"))
        ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_consume(queue='orders_queue', on_message_callback=on_message)

    print("Waiting for orders in 'orders_queue'...")
    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        channel.stop_consuming()
        connection.close()
