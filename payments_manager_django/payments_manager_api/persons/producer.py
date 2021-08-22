import os
import pika
import json


amqp_url: str = os.getenv("AMQP_URL")
params = pika.URLParameters(amqp_url)
connection = pika.BlockingConnection(params)
channel = connection.channel()


def publish(method, body):
    properties = pika.BasicProperties(method)
    channel.basic_publish(
        exchange="", routing_key="flask", body=json.dumps(body), properties=properties
    )
