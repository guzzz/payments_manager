import json
from flask import Flask
from flask_testing import TestCase
from datetime import date
from flask_sqlalchemy import SQLAlchemy

from main import app, db, Account, DailyDebit


class BaseTest(TestCase):
    def create_app(self):
        app = Flask(__name__)
        app.config["TESTING"] = True
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        db.init_app(app)
        app.app_context().push()
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()


class AccountUnitTest(BaseTest):
    def test_creation(self):
        try:
            account = Account(id=1)
            db.session.add(account)
            db.session.commit()
            self.assertIn(account, Account.query.all())
        except:
            self.assertEqual(True, False)


class DailyDebitUnitTest(BaseTest):
    def test_creation(self):
        today = date.today()
        try:
            daily_debit = DailyDebit(date=today, ammount=10.00, account_id=1)
            db.session.add(daily_debit)
            db.session.commit()
            self.assertIn(daily_debit, DailyDebit.query.all())
        except:
            self.assertEqual(True, False)


class TransactionCreditIntegrationTest(BaseTest):
    def test_success_credit(self):
        account = Account(
            id=1, balance=0.00, max_daily_withdraw=1000.00, active=True, type=1
        )
        db.session.add(account)
        db.session.commit()

        with app.test_client() as client:
            data = {"value": 100.00}
            response = client.post(
                "/api/accounts/1/credit/",
                headers={"Content-Type": "application/json"},
                data=json.dumps(data),
            )
            self.assertEqual(response.status_code, 201)

    def test_fail_credit_account_do_not_exist(self):
        with app.test_client() as client:
            data = {"value": 100.00}
            response = client.post(
                "/api/accounts/2147483647/credit/",
                headers={"Content-Type": "application/json"},
                data=json.dumps(data),
            )
            self.assertEqual(response.status_code, 404)


class TransactionDebitIntegrationTest(BaseTest):
    def setUp(self):
        super().setUp()
        account = Account(
            id=1, balance=5000.00, max_daily_withdraw=1500.00, active=True, type=1
        )
        db.session.add(account)
        db.session.commit()

    def test_success_debit(self):
        with app.test_client() as client:
            data = {"value": 1000.00}
            response = client.post(
                "/api/accounts/1/debit/",
                headers={"Content-Type": "application/json"},
                data=json.dumps(data),
            )
            self.assertEqual(response.status_code, 201)

    def test_account_not_found_debit(self):
        with app.test_client() as client:
            data = {"value": 1000.00}
            response = client.post(
                "/api/accounts/2/debit/",
                headers={"Content-Type": "application/json"},
                data=json.dumps(data),
            )
            self.assertEqual(response.status_code, 404)

    def test_account_inactive_debit(self):
        account = Account.query.get(1)
        account.active = False
        db.session.commit()
        with app.test_client() as client:
            data = {"value": 1000.00}
            response = client.post(
                "/api/accounts/1/debit/",
                headers={"Content-Type": "application/json"},
                data=json.dumps(data),
            )
            self.assertEqual(response.status_code, 403)

    def test_request_value_invalid_debit(self):
        with app.test_client() as client:
            data = {"value": "HI"}
            response = client.post(
                "/api/accounts/1/debit/",
                headers={"Content-Type": "application/json"},
                data=json.dumps(data),
            )
            self.assertEqual(response.status_code, 400)

    def test_requested_value_bigger_than_daily_withdraw_debit(self):
        with app.test_client() as client:
            data = {"value": 2000.00}
            response = client.post(
                "/api/accounts/1/debit/",
                headers={"Content-Type": "application/json"},
                data=json.dumps(data),
            )
            self.assertEqual(response.status_code, 403)

    def test_requested_value_bigger_than_balance(self):
        account = Account.query.get(1)
        account.balance = 500.00
        db.session.commit()
        with app.test_client() as client:
            data = {"value": 1000.00}
            response = client.post(
                "/api/accounts/1/debit/",
                headers={"Content-Type": "application/json"},
                data=json.dumps(data),
            )
            self.assertEqual(response.status_code, 403)
