from datetime import datetime
from django.test import TestCase

from payments_manager_api.persons.models import Person


class PersonUnitTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super(PersonUnitTest, cls).setUpClass()
        print("======================================================================")
        print("==> INITIALIZING Person UNIT Tests...")
        print("======================================================================")
        print("... CREATING initial configuration ..............................")

        benzemaoe = Person.objects.create(
            name="Karim Benzema", cpf="658.418.030-18", birth_date="2000-01-01"
        )
        print("----------------------------------------------------------------------")

    def test_create_person(self):
        print("==> Creating NEW person")
        try:
            vini_jr = Person.objects.create(
                name="Vini Jr.", cpf="161.127.550-41", birth_date="2000-01-01"
            )
            self.assertEqual(type(vini_jr), Person)
        except:
            self.assertEqual(False, True)
        print("----------------------------------------------------------------------")

    def test_create_person_with_repeated_cpf(self):
        print("==> Creating person with repeated CPF")
        try:
            benzemaoe = Person.objects.create(
                name="Karim Benzema", cpf="658.418.030-18", birth_date="2000-01-01"
            )
            self.assertEqual(False, True)
        except:
            self.assertEqual(True, True)
        print("----------------------------------------------------------------------")
