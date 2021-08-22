from rest_framework import serializers
from brazilnum.cpf import validate_cpf

from .models import Person


class PersonSerializer(serializers.ModelSerializer):
    cpf = serializers.CharField(max_length=14)

    class Meta:
        model = Person
        fields = "__all__"

    def validate_cpf(self, cpf):
        if not validate_cpf(cpf):
            raise serializers.ValidationError(
                "Invalid CPF. A valid CPF should also be organized as: 000.000.000-00"
            )
        else:
            person_registred = Person.objects.filter(cpf=cpf)
            if person_registred.exists():
                raise serializers.ValidationError(
                    "It is not possible to register more than one person with the same CPF."
                )
        return cpf
