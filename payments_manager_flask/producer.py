import os
import pika
import json
from dotenv import load_dotenv

load_dotenv()


amqp_url: str = os.getenv("AMQP_URL")
params = pika.URLParameters(amqp_url)
connection = pika.BlockingConnection(params)
channel = connection.channel()


def publish(method, body):
    properties = pika.BasicProperties(method)
    channel.basic_publish(
        exchange="", routing_key="django", body=json.dumps(body), properties=properties
    )
