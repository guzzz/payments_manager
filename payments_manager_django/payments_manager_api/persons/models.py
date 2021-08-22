from django.db import models


class Person(models.Model):
    name = models.CharField(max_length=150)
    cpf = models.CharField(max_length=14, unique=True)
    birth_date = models.DateField(null=False)
