# Entry point for the management-service
# app.py
from flask import Flask, jsonify
from threading import Thread
from services.rabbitmq_service import consume_orders
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

orders = []  # Temporary in-memory store for orders

# Route to get all orders
@app.route('/api/orders', methods=['GET'])
def get_orders():
    return jsonify(orders)

# Function to store orders received from RabbitMQ
def handle_new_order(order):
    orders.append(order)

# Start consuming RabbitMQ messages in a separate thread
def start_rabbitmq_consumer():
    consume_orders(handle_new_order)

if __name__ == '__main__':
    # Start RabbitMQ consumer in a background thread
    rabbitmq_thread = Thread(target=start_rabbitmq_consumer)
    rabbitmq_thread.start()

    # Run the Flask app
    port = int(os.getenv("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
