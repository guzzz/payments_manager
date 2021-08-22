import pika
import json
import os
import django

from decimal import Decimal
from dotenv import load_dotenv

load_dotenv()

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from payments_manager_api.accounts.models import Transaction, Account

amqp_url: str = os.getenv("AMQP_URL")
params = pika.URLParameters(amqp_url)

connection = pika.BlockingConnection(params)
channel = connection.channel()
channel.queue_declare(queue="django")


def callback(ch, method, properties, body):
    print("Received in django")
    data = json.loads(body)
    print(data)

    if properties.content_type == "debit_transaction":

        account = Account.objects.get(id=data.get("account_id"))
        value = Decimal(data.get("transaction_value")) * -1
        created = data.get("created")
        transaction = Transaction.objects.create(
            value=value, account=account, created=created
        )
        account.balance = data.get("account_balance")
        account.save()

        print("DEBIT Transaction CREATED!")

    elif "credit_transaction":

        account = Account.objects.get(id=data.get("account_id"))
        value = Decimal(data.get("transaction_value"))
        created = data.get("created")
        transaction = Transaction.objects.create(
            value=value, account=account, created=created
        )
        account.balance = data.get("account_balance")
        account.save()

        print("CREDIT Transaction CREATED!")


channel.basic_consume(queue="django", on_message_callback=callback, auto_ack=True)
print("Django queue up!")
channel.start_consuming()
channel.close()
