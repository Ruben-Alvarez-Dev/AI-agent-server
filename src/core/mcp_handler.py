# MCP Handler

import json
import pika
import threading
import time

from src.config.config_loader import config

class MCPHandler:
    def __init__(self):
        """
        Initializes the MCP Handler for RabbitMQ communication.
        """
        mcp_config = config.get("mcp_config", {})
        self.rabbitmq_host = mcp_config.get("rabbitmq_host", "localhost")
        self.connection = None
        self.channel = None
        self.consuming_thread = None
        self.callbacks = {}
        self.is_consuming = False
        print("MCP Handler initialized for RabbitMQ.")

    def connect(self):
        """
        Establishes a connection to the RabbitMQ broker.
        """
        if self.connection and self.connection.is_open:
            return

        try:
            print(f"Connecting to RabbitMQ broker at {self.rabbitmq_host}...")
            self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.rabbitmq_host))
            self.channel = self.connection.channel()
            print("Successfully connected to RabbitMQ broker.")
        except pika.exceptions.AMQPConnectionError as e:
            print(f"Error connecting to RabbitMQ: {e}")
            self.connection = None
            self.channel = None
            raise

    def publish_message(self, queue_name: str, message: dict):
        """
        Publishes a message to a specified RabbitMQ queue.
        """
        if not self.channel:
            print("MCP channel not available. Cannot publish message.")
            return

        try:
            self.channel.queue_declare(queue=queue_name, durable=True)
            self.channel.basic_publish(
                exchange='',
                routing_key=queue_name,
                body=json.dumps(message),
                properties=pika.BasicProperties(
                    delivery_mode=2,  # make message persistent
                ))
            print(f"Published to queue '{queue_name}': {json.dumps(message, indent=2)}")
        except Exception as e:
            print(f"Error publishing message to RabbitMQ: {e}")

    def subscribe_to_channel(self, queue_name: str, callback):
        """
        Registers a callback for a specific queue.
        """
        self.callbacks[queue_name] = callback
        print(f"Callback registered for queue '{queue_name}'.")
        if self.is_consuming and self.channel:
             # If already consuming, just declare the new queue and start consuming from it
            self.channel.queue_declare(queue=queue_name, durable=True)
            self.channel.basic_consume(queue=queue_name, on_message_callback=self._on_message, auto_ack=False)


    def _on_message(self, ch, method, properties, body):
        """Internal callback to dispatch messages to the correct handler."""
        queue_name = method.routing_key
        if queue_name in self.callbacks:
            try:
                self.callbacks[queue_name](body)
                ch.basic_ack(delivery_tag=method.delivery_tag)
            except Exception as e:
                print(f"Error processing message from '{queue_name}': {e}")
                ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False) # Move to DLQ if configured
        else:
            print(f"No callback registered for queue '{queue_name}'. Discarding message.")
            ch.basic_ack(delivery_tag=method.delivery_tag)

    def start_consuming(self):
        """
        Starts consuming messages from all subscribed queues in a separate thread.
        """
        if not self.channel:
            print("MCP channel not available. Cannot start consuming.")
            return

        if self.is_consuming:
            print("Already consuming messages.")
            return

        self.is_consuming = True
        self.consuming_thread = threading.Thread(target=self._consume_loop, daemon=True)
        self.consuming_thread.start()
        print("Started consuming messages in a background thread.")

    def _consume_loop(self):
        """The actual loop that consumes messages from RabbitMQ."""
        # Re-establish channel in the new thread
        local_connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.rabbitmq_host))
        local_channel = local_connection.channel()
        
        print("Consumer thread started.")
        for queue_name in self.callbacks.keys():
            local_channel.queue_declare(queue=queue_name, durable=True)
            local_channel.basic_consume(queue=queue_name, on_message_callback=self._on_message, auto_ack=False)
        
        try:
            local_channel.start_consuming()
        except Exception as e:
            print(f"Consumer thread encountered an error: {e}")
        finally:
            local_connection.close()
            print("Consumer thread stopped.")
            self.is_consuming = False


    def close(self):
        """
        Closes the connection to RabbitMQ.
        """
        if self.is_consuming and self.consuming_thread:
            self.is_consuming = False
            # The consumer is blocking, so we can't join it directly.
            # Pika recommends closing the connection from another thread.
            if self.connection and self.connection.is_open:
                self.connection.close()
            print("RabbitMQ connection closed.")
