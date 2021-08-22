from django.db import models
from decimal import Decimal


class Account(models.Model):
    balance = models.DecimalField(
        max_digits=16, decimal_places=2, default=Decimal("0.00")
    )
    max_daily_withdraw = models.DecimalField(
        max_digits=16, decimal_places=2, default=Decimal("0.00")
    )
    active = models.BooleanField(default=True)
    type = models.PositiveIntegerField(null=False, default=1)
    created = models.DateTimeField(auto_now_add=True)
    person = models.ForeignKey(
        to="persons.Person",
        related_name="%(class)s",
        null=False,
        on_delete=models.CASCADE,
    )


class Transaction(models.Model):
    value = models.DecimalField(max_digits=16, decimal_places=2)
    created = models.DateTimeField()
    account = models.ForeignKey(
        to=Account, related_name="%(class)s", null=False, on_delete=models.CASCADE
    )
