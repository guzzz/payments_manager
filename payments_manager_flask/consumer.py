import os
import pika
import json
import maya

from dotenv import load_dotenv
from main import Account, db

load_dotenv()


amqp_url: str = os.getenv("AMQP_URL")
params = pika.URLParameters(amqp_url)

connection = pika.BlockingConnection(params)
channel = connection.channel()
channel.queue_declare(queue="flask")


def callback(ch, method, properties, body):
    print("Received in flask")
    data = json.loads(body)
    print(data)

    if properties.content_type == "account_created":
        created_datetime = maya.parse(data.get("created")).datetime()
        account = Account(
            id=data.get("id"),
            balance=data.get("balance"),
            max_daily_withdraw=data.get("max_daily_withdraw"),
            active=data.get("active"),
            type=data.get("type"),
            created=created_datetime,
        )
        db.session.add(account)
        db.session.commit()
        print("Account Created!")

    elif properties.content_type == "account_active_flag_updated":
        account = Account.query.get(data.get("account_id"))
        account.active = data.get("active_flag")
        db.session.commit()
        print("Account Active Flag Updated!")


channel.basic_consume(queue="flask", on_message_callback=callback, auto_ack=True)
print("Flask queue up!")
channel.start_consuming()
channel.close()
