from datetime import datetime
from django.test import TestCase

from payments_manager_api.accounts.models import Account, Transaction
from payments_manager_api.persons.models import Person


class AccountUnitTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super(AccountUnitTest, cls).setUpClass()
        print("======================================================================")
        print("==> INITIALIZING Account UNIT Tests...")
        print("======================================================================")
        print("... CREATING initial configuration ..............................")

        initial_user = Person.objects.create(
            name="Vini Jr.", cpf="754.372.640-89", birth_date="2000-01-01"
        )
        print("----------------------------------------------------------------------")

    def test_create_account(self):
        print("==> Creating NEW account")
        try:
            new_account = Account.objects.create(person=Person.objects.all().first())
            self.assertEqual(type(new_account), Account)
        except:
            self.assertEqual(False, True)
        print("----------------------------------------------------------------------")

    def test_inactivate_account(self):
        print("==> Inactivate account")
        try:
            new_account = Account.objects.create(
                active=True, person=Person.objects.all().first()
            )
            new_account.active = False
            new_account.save()
            self.assertEqual(new_account.active, False)
        except:
            self.assertEqual(False, True)
        print("----------------------------------------------------------------------")

    def test_activate_account(self):
        print("==> Activate account")
        try:
            new_account = Account.objects.create(
                active=False, person=Person.objects.all().first()
            )
            new_account.active = True
            new_account.save()
            self.assertEqual(new_account.active, True)
        except:
            self.assertEqual(False, True)
        print("----------------------------------------------------------------------")


class TransactionUnitTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super(TransactionUnitTest, cls).setUpClass()
        print("======================================================================")
        print("==> INITIALIZING Transaction UNIT Tests...")
        print("======================================================================")
        print("... CREATING initial configuration ..............................")

        initial_user = Person.objects.create(
            name="Vini Jr.", cpf="245.959.500-04", birth_date="2000-01-01"
        )
        initial_account = Account.objects.create(person=initial_user)

        print("----------------------------------------------------------------------")

    def test_create_new_transaction(self):
        print("==> Creating NEW transaction")
        try:
            new_transaction = Transaction.objects.create(
                value=1000.00,
                created=datetime.now(),
                account=Account.objects.all().first(),
            )
            self.assertEqual(type(new_transaction), Transaction)
        except:
            self.assertEqual(False, True)
        print("----------------------------------------------------------------------")
