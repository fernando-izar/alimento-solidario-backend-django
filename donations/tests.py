from rest_framework.test import APITestCase
from .models import Donations
from rest_framework.views import status
from django.urls import reverse
from model_bakery import baker
from users.models import User
from classifications.models import Classification
import ipdb

class DonationsTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.user = baker.make(User, type="donor", email="kenzinho@email.com", password="123456")
        cls.user.set_password(cls.user.password)
        cls.user.save()
        cls.classification1 = baker.make(Classification, name="Laticínio")
        cls.classification2 = baker.make(Classification, name="Sucos")
        cls.classification3 = baker.make(Classification, name="Frutas")

    def test_donation_creation_without_required_fields(self):
        data_login = {'email': self.user.email, 'password': '123456'}
        url_login = reverse('login')
        response_login = self.client.post(url_login, data_login)
        user_token = response_login.data['token']
        headers = {"HTTP_AUTHORIZATION": f'Bearer {user_token}'}

        url = reverse('donations')
        response = self.client.post(url, data={}, format="json", **headers)

        # STATUS CODE
        expected_status_code = status.HTTP_400_BAD_REQUEST
        resulted_status_code = response.status_code
        msg = (
            "Verifique se o status code retornado do POST sem todos os campos obrigatórios"
            + f" em `{url}` é {expected_status_code}"
        )
        """ self.assertEqual(expected_status_code, resulted_status_code, msg) """

        # RETORNO JSON
        resulted_data: dict = response.json()
        expected_fields = {
            "food",
            "quantity",
            "expiration",
            "classification",
        }
        returned_fields = set(resulted_data.keys())
        msg = "blablabla"
        self.assertSetEqual(expected_fields, returned_fields, msg)

    """ def test_creation_donation(self):
        data_login = {'email': self.user.email, 'password': '123456'}
        url_login = reverse('login')
        response_login = self.client.post(url_login, data_login)
        user_token = response_login.data['token']
        headers = {"HTTP_AUTHORIZATION": f'Bearer {user_token}'}

        url_donation = reverse('donations')
        data_donation = {"food": "amoras silvestres", "quantity": "10 caixas", "expiration": "12/12/2022", "classification": f'{self.classification.id}'}
        response_donation = self.client.post(url_donation, data_donation, **headers)

        resulted_data = response_donation.json()
        expected_fields = {'id', 'food', 'quantity', 'expiration', 'classification', 'user', 'available', 'createdAt', 'updatedAt'}
        returned_fields = set(resulted_data.keys())
        message1 = 'bla'
        self.assertEqual(expected_fields, returned_fields, msg=message1)

        expected_status = status.HTTP_201_CREATED
        resulted_status = response_donation.status_code
        message2 = "blablabla"
        self.assertEqual(expected_status, resulted_status, msg=message2) """
    
    """ def test_list_donation(self):
        data_login = {'email': self.user.email, 'password': '123456'}
        url_login = reverse('login')
        response_login = self.client.post(url_login, data_login)
        user_token = response_login.data['token']
        headers = {"HTTP_AUTHORIZATION": f'Bearer {user_token}'}

        url_donation = reverse('donations')
        data_donation1 = baker.make(Donations, expiration='2023-01-10', classification={self.classification1.id})
        data_donation2 = baker.make(Donations, expiration='2023-01-10', classification={self.classification2.id})
        data_donation3 = baker.make(Donations, expiration='2023-01-10', classification={self.classification3.id})
        self.client.post(url_donation, data_donation1, **headers)
        self.client.post(url_donation, data_donation2, **headers)
        self.client.post(url_donation, data_donation3, **headers)

        response_donation_get = self.client.get(url_donation, **headers)
        message = "Verify listing donations"
        self.assertEqual(len(response_donation_get.data), 3, msg=message)
 """

