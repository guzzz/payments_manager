import simplejson

from flask import Flask, jsonify, request
from flask_cors import CORS

from models.all_models import db, Account, DailyDebit
from utils.dates import *
from utils.validations import *
from producer import publish

app = Flask(__name__)
app.config["TESTING"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:root@db/main"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
CORS(app)

db.init_app(app)
app.app_context().push()


@app.route("/", methods=["GET"])
def hello():
    return jsonify({"message": "Flask Transaction Services UP!"})


@app.route("/api/accounts/<int:account_id>/debit/", methods=["POST"])
def debit(account_id):
    return create_transaction(account_id, "debit_transaction")


@app.route("/api/accounts/<int:account_id>/credit/", methods=["POST"])
def credit(account_id):
    return create_transaction(account_id, "credit_transaction")


def create_transaction(account_id, transaction_type):
    data = request.json
    account = Account.query.get_or_404(account_id)

    if not is_valid_account(account):
        response = {
            "message": "An inactive account is not allowed to receive transactions."
        }
        return jsonify(response), 403

    valid_request, info_after_validation, created = is_valid_request(data)
    if valid_request:
        transaction_value = info_after_validation
    else:
        return jsonify(info_after_validation), 400

    if transaction_type == "credit_transaction":
        account.balance = account.balance + transaction_value
    else:
        if debit_is_allowed(account, transaction_value, created):
            account.balance = account.balance - transaction_value
        else:
            response = {
                "message": "Debit is not allowed! Please check your balance and daily withdraw limits."
            }
            return (jsonify(response), 403)

    db.session.commit()
    publish_transaction(transaction_value, account, created, transaction_type)
    return jsonify({"message": "success"}), 201


def debit_is_allowed(account, ammount, transaction_datetime):
    transaction_date = convert_datetime_to_date(transaction_datetime)
    daily_debit = DailyDebit.query.filter(
        DailyDebit.date == transaction_date, DailyDebit.account_id == account.id
    ).first()
    if daily_debit:
        total_debit = daily_debit.ammount + ammount
        if account.max_daily_withdraw < total_debit:
            return False
        else:
            if debit_bigger_than_account_balance(account, ammount):
                return False
            else:
                daily_debit.ammount = total_debit
                return True
    else:
        if account.max_daily_withdraw < ammount:
            return False
        else:
            if debit_bigger_than_account_balance(account, ammount):
                return False
            else:
                daily_debit = DailyDebit(
                    date=transaction_date, ammount=ammount, account_id=account.id
                )
                db.session.add(daily_debit)
                return True


def publish_transaction(value, account, created, transaction_type):
    if not app.config["TESTING"]:
        info = {
            "transaction_value": simplejson.dumps(value),
            "account_id": account.id,
            "account_balance": simplejson.dumps(account.balance),
            "created": str(created),
        }
        publish(transaction_type, info)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
