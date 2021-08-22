import json
from datetime import date
from rest_framework.test import APITestCase

from payments_manager_api.accounts.models import Account, Transaction
from payments_manager_api.persons.models import Person


class AccountIntegrationTest(APITestCase):
    @classmethod
    def setUpClass(cls):
        super(AccountIntegrationTest, cls).setUpClass()
        print("======================================================================")
        print("==> INITIALIZING Account INTEGRATION Tests...")
        print("======================================================================")
        print("... CREATING initial configuration ..............................")

        initial_user = Person.objects.create(
            name="Vini Jr.", cpf="936.141.520-49", birth_date="2000-01-01"
        )
        initial_account = Account.objects.create(active=True, person=initial_user)

        print("----------------------------------------------------------------------")

    def test_list_accounts(self):
        print("==> LIST: [GET] /accounts/")
        response = self.client.get("/accounts/")
        self.assertEqual(response.status_code, 200)
        print("----------------------------------------------------------------------")

    def test_retrieve_account(self):
        print("==> LIST: [GET] /accounts/ID/")
        account_id = str(Account.objects.all().first().id)
        response = self.client.get(f"/accounts/{account_id}/")
        self.assertEqual(response.status_code, 200)
        print("----------------------------------------------------------------------")

    def test_inactivate_account(self):
        print("==> LIST: [GET] /accounts/ID/inactivate")
        account_id = str(Account.objects.all().first().id)
        response = self.client.get(f"/accounts/{account_id}/inactivate/")
        self.assertEqual(response.status_code, 200)
        response = self.client.get(f"/accounts/{account_id}/")
        self.assertEqual(response.data.get("active"), False)
        print("----------------------------------------------------------------------")

    def test_activate_account(self):
        print("==> LIST: [GET] /accounts/ID/activate")
        person = Person.objects.all().first()
        account_id = Account.objects.create(active=False, person=person).id
        response = self.client.get(f"/accounts/{account_id}/activate/")
        self.assertEqual(response.status_code, 200)
        response = self.client.get(f"/accounts/{account_id}/")
        self.assertEqual(response.data.get("active"), True)
        print("----------------------------------------------------------------------")

    def test_get_account_balance(self):
        print("==> LIST: [GET] /accounts/ID/balance/")
        account_id = str(Account.objects.all().first().id)
        response = self.client.get(f"/accounts/{account_id}/balance/")
        self.assertEqual(response.status_code, 200)
        print("----------------------------------------------------------------------")

    def test_create_account(self):
        print("==> CREATE: [POST] /accounts/")
        data = {"person": str(Person.objects.all().first().id)}
        response = self.client.post(
            "/accounts/", data=json.dumps(data), content_type="application/json"
        )
        self.assertEqual(response.status_code, 201)
        print("----------------------------------------------------------------------")
