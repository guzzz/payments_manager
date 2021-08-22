
from marshmallow import Schema, fields


class TransactionForm(Schema):
    value = fields.Decimal(required=True, places=2)
    created = fields.DateTime(required=False)
