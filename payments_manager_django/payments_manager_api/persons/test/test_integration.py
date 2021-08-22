import json
from datetime import date
from rest_framework.test import APITestCase

from payments_manager_api.accounts.models import Account, Transaction
from payments_manager_api.persons.models import Person


class PersonIntegrationTest(APITestCase):
    @classmethod
    def setUpClass(cls):
        super(PersonIntegrationTest, cls).setUpClass()
        print("======================================================================")
        print("==> INITIALIZING Person INTEGRATION Tests...")
        print("======================================================================")
        print("... CREATING initial configuration ..............................")

        initial_user = Person.objects.create(
            name="Vini Jr.", cpf="936.141.520-49", birth_date="2000-01-01"
        )

        print("----------------------------------------------------------------------")

    def test_list_persons(self):
        print("==> LIST: [GET] /persons/")
        response = self.client.get("/persons/")
        self.assertEqual(response.status_code, 200)
        print("----------------------------------------------------------------------")

    def test_retrieve_persons(self):
        print("==> LIST: [GET] /persons/ID/")
        person_id = str(Person.objects.all().first().id)
        response = self.client.get(f"/persons/{person_id}/")
        self.assertEqual(response.status_code, 200)
        print("----------------------------------------------------------------------")

    def test_create_person(self):
        print("==> CREATE: [POST] /persons/")
        data = {
            "name": "Menino Ney",
            "cpf": "997.998.900-98",
            "birth_date": "2000-01-01",
        }
        response = self.client.post(
            "/persons/", data=json.dumps(data), content_type="application/json"
        )
        self.assertEqual(response.status_code, 201)
        print("----------------------------------------------------------------------")

    def test_create_person_with_same_cpf(self):
        print("==> CREATE: [POST] /persons/")
        data = {
            "name": "Menino Ney",
            "cpf": "936.141.520-49",
            "birth_date": "2000-01-01",
        }
        response = self.client.post(
            "/persons/", data=json.dumps(data), content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)
        print("----------------------------------------------------------------------")
