from datetime import datetime


def convert_datetime_to_date(transaction_datetime):
    if type(transaction_datetime) is str:
        transaction_datetime = datetime.strptime(
            transaction_datetime, "%Y-%m-%d %H:%M:%S"
        )
    return transaction_datetime.date()