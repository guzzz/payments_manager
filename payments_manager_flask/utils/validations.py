from datetime import date, datetime

from schemas.transaction_form import TransactionForm
from marshmallow import ValidationError


def debit_bigger_than_account_balance(account, debit):
    if account.balance < debit:
        return True
    else:
        return False


def is_valid_account(account):
    if account.active:
        return True
    else:
        return False


def is_valid_request(data):
    schema = TransactionForm()
    try:
        body = schema.load(data)
        value = body.get("value")
        if value <= 0.00:
            return (
                False,
                {"message": "This operation only accepts positive numbers."},
                None,
            )

        created = body.get("created", False)
        if not created:
            created = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        return True, value, created
    except ValidationError as err:
        return False, err.messages, None
