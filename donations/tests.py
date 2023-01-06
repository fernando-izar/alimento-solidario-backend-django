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
        cls.DONATION_URL = "/api/donations/"
        cls.LOGIN_URL = "/api/login/"
        cls.user = baker.make(User, type="donor", email="kenzinho@email.com", password="123456", isAdm=True)
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

        resulted_data = response.json()
        expected_fields = {
            "food",
            "quantity",
            "expiration",
            "classification",            
            }
        returned_fields = set(resulted_data.keys())
        msg = "Verify if all required keys are returned with an ampty donation creation request"
        self.assertEqual(expected_fields, returned_fields, msg=msg)

        expected_status_code = status.HTTP_400_BAD_REQUEST
        resulted_status_code = response.status_code
        msg=("Verify if the status code is 400 when trying to create a donation without required fields")
        self.assertEqual(expected_status_code, resulted_status_code, msg=msg)

    def test_creation_donation(self):
        data_login = {'email': self.user.email, 'password': '123456'}
        url_login = reverse('login')
        response_login = self.client.post(url_login, data_login)
        user_token = response_login.data['token']
        headers = {"HTTP_AUTHORIZATION": f'Bearer {user_token}'}

        url_donation = reverse('donations')
        data_donation = {"food": "amoras silvestres", "quantity": "10 caixas", "expiration": "2023-12-12", "classification": f'{self.classification1.id}'}
        response_donation = self.client.post(url_donation, data_donation, **headers)

        resulted_data = response_donation.json()
        expected_fields = {'id', 'food', 'quantity', 'expiration', 'classification', 'user', 'available', 'createdAt', 'updatedAt'}
        returned_fields = set(resulted_data.keys())
        message1 = 'bla'
        self.assertEqual(expected_fields, returned_fields, msg=message1)

        expected_status = status.HTTP_201_CREATED
        resulted_status = response_donation.status_code
        message2 = "blablabla"
        self.assertEqual(expected_status, resulted_status, msg=message2)
    
    def test_list_donation(self):
        data_login = {'email': self.user.email, 'password': '123456'}
        url_login = reverse('login')
        response_login = self.client.post(url_login, data_login)
        user_token = response_login.data['token']
        headers = {"HTTP_AUTHORIZATION": f'Bearer {user_token}'}

        url_donation = reverse('donations')
        data_donation1 = {"food": "amoras silvestres", "quantity": "10 caixas", "expiration": "2023-12-12", "classification": f'{self.classification1.id}'}
        data_donation2 = {"food": "amoras silvestres", "quantity": "10 caixas", "expiration": "2023-12-12", "classification": f'{self.classification2.id}'}
        data_donation3 = {"food": "amoras silvestres", "quantity": "10 caixas", "expiration": "2023-12-12", "classification": f'{self.classification3.id}'}
        response = self.client.post(url_donation, data_donation1, **headers)
        self.client.post(url_donation, data_donation2, **headers)
        self.client.post(url_donation, data_donation3, **headers)

        response_donation_get = self.client.get(url_donation, **headers)
        message = "Verify listing donations"
        ipdb.set_trace()
        self.assertEqual(len(response_donation_get.data), 3, msg=message)

    def test_cannot_list_donation_by_id_without_authentication(self):

        donation = baker.make(Donations)
        url = f"{self.DONATION_URL}{donation.id}/"

        response = self.client.get(url)

        expected_status_code = status.HTTP_401_UNAUTHORIZED
        resulted_status_code = response.status_code
        msg = "Verify if the status code is 401 when trying to list a user without authentication"
        self.assertEqual(expected_status_code, resulted_status_code, msg=msg)

    def test_cannot_list_all_donations_without_authentication(self):
        baker.make(Donations, _quantity=10)

        response = self.client.get(self.DONATION_URL)

        expected_status_code = status.HTTP_401_UNAUTHORIZED
        resulted_status_code = response.status_code
        msg = "Verify if the status code is 401 when trying to list all donations without authentication"
        self.assertEqual(expected_status_code, resulted_status_code, msg=msg)

        expected_response = {"detail": "Authentication credentials were not provided."}
        resulted_response = response.data
        msg = "Verify if the response is the expected when trying to list all donations without authentication"
        self.assertEqual(expected_response, resulted_response, msg=msg)

    def test_cannot_delete_donation_by_id_without_authentication(self):
        donation = baker.make(Donations)
        url = f"{self.DONATION_URL}{donation.id}/"

        response = self.client.delete(url)

        expected_status_code = status.HTTP_401_UNAUTHORIZED
        resulted_status_code = response.status_code
        msg = "Verify if the status code is 401 when trying to delete a donation without authentication"
        self.assertEqual(expected_status_code, resulted_status_code, msg=msg)

        expected_response = {"detail": "Authentication credentials were not provided."}
        resulted_response = response.data
        msg = "Verify if the response is the expected when trying to delete a donation without authentication"
        self.assertEqual(expected_response, resulted_response, msg=msg)

    def test_cannot_update_donation_by_id_without_authentication(self):
        donation = baker.make(Donations)

        data = {"food": "Teste"}
        url = f"{self.DONATION_URL}{donation.id}/"
        response = self.client.patch(url, data)
        expected_status_code = status.HTTP_401_UNAUTHORIZED
        resulted_status_code = response.status_code
        msg = "Verify if the status code is 401 when trying to update a donation without authentication"
        self.assertEqual(expected_status_code, resulted_status_code, msg=msg)

        expected_response = {"detail": "Authentication credentials were not provided."}
        resulted_response = response.data
        msg = "Verify if the response is the expected when trying to update a donation without authentication"
        self.assertEqual(expected_response, resulted_response, msg=msg)

    def test_cannot_update_donation_by_id_with_invalid_id(self):
        data_login = {'email': self.user.email, 'password': '123456'}
        url_login = reverse('login')
        response_login = self.client.post(url_login, data_login)
        user_token = response_login.data['token']
        headers = {"HTTP_AUTHORIZATION": f'Bearer {user_token}'}

        data = {"food": "Updated"}
        url = f"{self.DONATION_URL}invalid_id/"
        response = self.client.patch(url, data, **headers)
        expected_status_code = status.HTTP_404_NOT_FOUND
        resulted_status_code = response.status_code
        msg = "Verify if the status code is 404 when trying to update a donation with invalid id"
        self.assertEqual(expected_status_code, resulted_status_code, msg=msg)

        expected_response = {"detail": "Not found."}
        resulted_response = response.data
        msg = "Verify if the response is the expected when trying to update a donation with invalid id"
        self.assertEqual(expected_response, resulted_response, msg=msg)

    def test_cannot_list_donation_by_id_with_invalid_id(self):
        data_login = {'email': self.user.email, 'password': '123456'}
        url_login = reverse('login')
        response_login = self.client.post(url_login, data_login)
        user_token = response_login.data['token']
        headers = {"HTTP_AUTHORIZATION": f'Bearer {user_token}'}

        donation = baker.make(Donations)

        url = f"{self.DONATION_URL}invalid_id/"
        response = self.client.patch(url, **headers)
        expected_status_code = status.HTTP_404_NOT_FOUND
        resulted_status_code = response.status_code
        msg = "Verify if the status code is 404 when trying to update a donation with invalid id"
        self.assertEqual(expected_status_code, resulted_status_code, msg=msg)

        expected_response = {"detail": "Not found."}
        resulted_response = response.data
        msg = "Verify if the response is the expected when trying to update a donation with invalid id"
        self.assertEqual(expected_response, resulted_response, msg=msg)

    def test_delete_donation(self):
        donation = baker.make(Donations)
        url = f"{self.DONATION_URL}{donation.id}/"

        data_login = {'email': self.user.email, 'password': '123456'}
        url_login = reverse('login')
        response_login = self.client.post(url_login, data_login)
        user_token = response_login.data['token']
        headers = {"HTTP_AUTHORIZATION": f'Bearer {user_token}'}

        response = self.client.delete(url, **headers)

        expected_status_code = status.HTTP_204_NO_CONTENT
        resulted_status_code = response.status_code
        msg = "Verify if the status code is 204 when trying to delete a donation"
        self.assertEqual(expected_status_code, resulted_status_code, msg=msg)        

    def test_update_donation(self):
        data_login = {'email': self.user.email, 'password': '123456'}
        url_login = reverse('login')
        response_login = self.client.post(url_login, data_login)
        user_token = response_login.data['token']
        headers = {"HTTP_AUTHORIZATION": f'Bearer {user_token}'}

        donation = baker.make(Donations)

        data = {"food": "Test Updated"}
        url = f"{self.DONATION_URL}{donation.id}/"
        response = self.client.patch(url, data, **headers)

        expected_status_code = status.HTTP_200_OK
        resulted_status_code = response.status_code
        msg = "Verify if the status code is 200 when trying to update a donation"
        self.assertEqual(expected_status_code, resulted_status_code, msg=msg)

        expected_response = 'Test Updated'
        resulted_response = response.data
        msg = "Verify if the response is the expected when trying to update a donation"
        self.assertEqual(expected_response, resulted_response['food'], msg=msg)

    def test_list_donation_by_id(self):
        data_login = {'email': self.user.email, 'password': '123456'}
        url_login = reverse('login')
        response_login = self.client.post(url_login, data_login)
        user_token = response_login.data['token']
        headers = {"HTTP_AUTHORIZATION": f'Bearer {user_token}'}

        donation = baker.make(Donations)
        url = f"{self.DONATION_URL}{donation.id}/"

        response = self.client.get(url, **headers)

        expected_status_code = status.HTTP_200_OK
        resulted_status_code = response.status_code
        msg = "Verify if the status code is 200 when trying to list a donation"
        self.assertEqual(expected_status_code, resulted_status_code, msg=msg)

        resulted_data = response.json()
        expected_fields = {'id', 'food', 'quantity', 'expiration', 'classification', 'user', 'available', 'createdAt', 'updatedAt'}
        returned_fields = set(resulted_data.keys())
        msg = 'Verify if all fields are returning'
        self.assertEqual(expected_fields, returned_fields, msg=msg)

    def test_delete_donation_by_invalid_id(self):
        data_login = {'email': self.user.email, 'password': '123456'}
        url_login = reverse('login')
        response_login = self.client.post(url_login, data_login)
        user_token = response_login.data['token']
        headers = {"HTTP_AUTHORIZATION": f'Bearer {user_token}'}

        url = f"{self.DONATION_URL}invalid_id/"
        response = self.client.delete(url, **headers)
        expected_status_code = status.HTTP_404_NOT_FOUND
        resulted_status_code = response.status_code
        msg = "Verify if the status code is 404 when trying to delete a donation with invalid id"
        self.assertEqual(expected_status_code, resulted_status_code, msg=msg)

        expected_response = {"detail": "Not found."}
        resulted_response = response.data
        msg = "Verify if the response is the expected when trying to delete a donation with invalid id"
        self.assertEqual(expected_response, resulted_response, msg=msg)