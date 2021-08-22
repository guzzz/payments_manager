
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    balance = db.Column(db.Numeric(16, 2))
    max_daily_withdraw = db.Column(db.Numeric())
    active = db.Column(db.Boolean())
    type = db.Column(db.Integer)
    created = db.Column(db.DateTime())
    daily_debt = db.relationship("DailyDebit", backref="daily_debit", lazy=True)


class DailyDebit(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.Date)
    ammount = db.Column(db.Numeric(16, 2))
    account_id = db.Column(db.Integer, db.ForeignKey("account.id"), nullable=False)
