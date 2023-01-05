from django.test import TestCase
from rest_framework.test import APITestCase
from model_bakery import baker
from rest_framework.views import status
from users.models import User
from addresses.models import Address
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractBaseUser
from django.urls import reverse
import pdb


User: AbstractBaseUser = get_user_model()


class UserRegisterViewTest(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.BASE_URL = "/api/users/"
        cls.LOGIN_URL = "/api/login/"

    # Verify if the keys returned are the expected when creating a user without required fields
    def test_user_creation_without_required_fields(self):
        response = self.client.post(self.BASE_URL, data={}, format="json")

        resulted_data = response.json()
        expected_fields = {"email", "name", "cnpj_cpf", "responsible", "contact", "address","password"}
        returned_fields = set(resulted_data.keys())
        msg = "Verify if all requred keys are returned with an ampty user creation request"
        self.assertEqual(expected_fields, returned_fields, msg=msg)

        expected_status_code = status.HTTP_400_BAD_REQUEST
        resulted_status_code = response.status_code
        msg=("Verify if the status code is 400 when trying to create a user without required fields")
        self.assertEqual(expected_status_code, resulted_status_code, msg=msg)

    # Verify if cannot create a user with an existing email
    def test_cannot_create_user_with_existing_email(self):
        user = baker.make(User, email="existing@mail.com")

        with self.assertRaises(Exception):
            baker.make(User, email="existing@mail.com")

    # Verify if cannot create a user with an existing cnpj_cpf
    def test_cannot_create_user_with_existing_cnpj_cpf(self):
        baker.make(User, cnpj_cpf="123456")

        with self.assertRaises(Exception):
            baker.make(User, cnpj_cpf="123456")
        
    # Verify if cannot list user by id without authentication
    def test_cannot_list_user_by_id_without_authentication(self):
        user = baker.make(User)
        url = f"{self.BASE_URL}{user.id}/"

        response = self.client.get(url)

        expected_status_code = status.HTTP_401_UNAUTHORIZED
        resulted_status_code = response.status_code
        msg = "Verify if the status code is 401 when trying to list a user without authentication"
        self.assertEqual(expected_status_code, resulted_status_code, msg=msg)

    # Verify if cannot list another user by id without admin authentication
    def test_cannot_list_another_user_by_id_without_admin_authentication(self):
        normal_user = baker.make(User, isAdm=False, password="123456", email="test@mail.com", type="donor")
        normal_user.set_password(normal_user.password)
        normal_user.save()

        url = reverse("login")
        data = {"email": "test@mail.com", "password": "123456"}
        response = self.client.post(url, data)
        # pdb.set_trace()
        normal_user_token = response.data["token"]

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {normal_user_token}")

        admin_user = baker.make(User, isAdm=True)
        admin_user.set_password(admin_user.password)
        admin_user.save()
        url = f"{self.BASE_URL}{admin_user.id}/"
        response = self.client.get(url)

        expected_status_code = status.HTTP_403_FORBIDDEN
        resulted_status_code = response.status_code
        msg = "Verify if the status code is 403 when trying to list another user's information with a non-admin token"
        self.assertEqual(expected_status_code, resulted_status_code, msg=msg)

        expected_response = {"detail": "You do not have permission to perform this action."}
        resulted_response = response.data
        msg = "Verify if the response is the expected when trying to list a user without admin authentication"
        self.assertEqual(expected_response, resulted_response, msg=msg)

    # Verify if cannot list all users without authentication
    def test_cannot_list_all_users_without_authentication(self):
        baker.make(User, _quantity=10)

        response = self.client.get(self.BASE_URL)

        expected_status_code = status.HTTP_401_UNAUTHORIZED
        resulted_status_code = response.status_code
        msg = "Verify if the status code is 401 when trying to list all users without authentication"
        self.assertEqual(expected_status_code, resulted_status_code, msg=msg)

        expected_response = {"detail": "Authentication credentials were not provided."}
        resulted_response = response.data
        msg = "Verify if the response is the expected when trying to list all users without authentication"
        self.assertEqual(expected_response, resulted_response, msg=msg)

    # Verify if cannot list all users without admin authentication
    def test_cannot_list_all_users_without_admin_authentication(self):
        normal_user = baker.make(User, isAdm=False, password="123456", email="test@mail.com", type="donor")
        normal_user.set_password(normal_user.password)
        normal_user.save()

        url = reverse("login")
        data = {"email": "test@mail.com", "password": "123456"}
        response = self.client.post(url, data)
        normal_user_token = response.data["token"]

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {normal_user_token}")

        admin_user = baker.make(User, isAdm=True)
        admin_user.set_password(admin_user.password)
        admin_user.save()
        url = f"{self.BASE_URL}{admin_user.id}/"
        response = self.client.get(url)

        expected_status_code = status.HTTP_403_FORBIDDEN
        resulted_status_code = response.status_code
        msg = "Verify if the status code is 403 when trying to list another user's information with a non-admin token"
        self.assertEqual(expected_status_code, resulted_status_code, msg=msg)

        expected_response = {"detail": "You do not have permission to perform this action."}
        resulted_response = response.data
        msg = "Verify if the response is the expected when trying to list a user without admin authentication"
        self.assertEqual(expected_response, resulted_response, msg=msg)

    # Verify if cannot delete user by id without authentication
    def test_cannot_delete_user_by_id_without_authentication(self):
        user = baker.make(User)
        url = f"{self.BASE_URL}{user.id}/"

        response = self.client.delete(url)

        expected_status_code = status.HTTP_401_UNAUTHORIZED
        resulted_status_code = response.status_code
        msg = "Verify if the status code is 401 when trying to delete a user without authentication"
        self.assertEqual(expected_status_code, resulted_status_code, msg=msg)

        expected_response = {"detail": "Authentication credentials were not provided."}
        resulted_response = response.data
        msg = "Verify if the response is the expected when trying to delete a user without authentication"
        self.assertEqual(expected_response, resulted_response, msg=msg)

    # Verify if cannot delete another user by id without admin authentication
    def test_cannot_delete_another_user_by_id_without_admin_authentication(self):
        normal_user = baker.make(User, isAdm=False, password="123456", email="test@mail.com", type="donor")
        normal_user.set_password(normal_user.password)
        normal_user.save()

        url = reverse("login")
        data = {"email": "test@mail.com", "password": "123456"}
        response = self.client.post(url, data)
        normal_user_token = response.data["token"]

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {normal_user_token}")

        admin_user = baker.make(User, isAdm=True)
        admin_user.set_password(admin_user.password)
        admin_user.save()
        url = f"{self.BASE_URL}{admin_user.id}/"
        response = self.client.delete(url)

        expected_status_code = status.HTTP_403_FORBIDDEN
        resulted_status_code = response.status_code
        msg = "Verify if the status code is 403 when trying to delete another user without admin authentication"
        self.assertEqual(expected_status_code, resulted_status_code, msg=msg)

        expected_response = {"detail": "You do not have permission to perform this action."}
        resulted_response = response.data
        msg = "Verify if the response is the expected when trying to delete another user without admin authentication"
        self.assertEqual(expected_response, resulted_response, msg=msg)

    # Verify if cannot update user by id without authentication
    def test_cannot_update_user_by_id_without_authentication(self):
        user = baker.make(User, type="donor", email="test@mail.com", password="123456")
        user.set_password(user.password)
        user.save()

        data = {"name": "Teste"}
        url = f"{self.BASE_URL}{user.id}/"
        response = self.client.patch(url, data)
        expected_status_code = status.HTTP_401_UNAUTHORIZED
        resulted_status_code = response.status_code
        msg = "Verify if the status code is 401 when trying to update a user without authentication"
        self.assertEqual(expected_status_code, resulted_status_code, msg=msg)

        expected_response = {"detail": "Authentication credentials were not provided."}
        resulted_response = response.data
        msg = "Verify if the response is the expected when trying to update a user without authentication"
        self.assertEqual(expected_response, resulted_response, msg=msg)

    # Verify if cannot update another user by id without admin authentication
    def test_cannot_update_another_user_by_id_without_admin_authentication(self):
        normal_user = baker.make(User, isAdm=False, password="123456", email="test@mail.com", type="donor")
        normal_user.set_password(normal_user.password)
        normal_user.save()

        url = reverse("login")
        data = {"email": "test@mail.com", "password": "123456"}
        response = self.client.post(url, data)
        normal_user_token = response.data["token"]

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {normal_user_token}")

        admin_user = baker.make(User, isAdm=True)
        admin_user.set_password(admin_user.password)
        admin_user.save()
        url = f"{self.BASE_URL}{admin_user.id}/"
        data = {"name": "Updated"}
        response = self.client.patch(url, data)

        expected_status_code = status.HTTP_403_FORBIDDEN
        resulted_status_code = response.status_code
        msg = "Verify if the status code is 403 when trying to update another user without admin authentication"
        self.assertEqual(expected_status_code, resulted_status_code, msg=msg)

        expected_response = {"detail": "You do not have permission to perform this action."}
        resulted_response = response.data
        msg = "Verify if the response is the expected when trying to update another user without admin authentication"
        self.assertEqual(expected_response, resulted_response, msg=msg)

    # Verify if cannot update user by id with invalid id
    def test_cannot_update_user_by_id_with_invalid_id(self):
        user = baker.make(User, type="donor", email="test@mail.com", password="123456", isAdm=True)
        user.set_password(user.password)
        user.save()

        url = reverse("login")
        data = {"email": "test@mail.com", "password": "123456"}
        response = self.client.post(url, data)
        user_token = response.data["token"]

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {user_token}")
        # headers = {"AUTHORIZATION": f"Bearer {user_token}"}
        data = {"name": "Updated"}
        url = f"{self.BASE_URL}invalid_id/"
        response = self.client.patch(url, data)
        expected_status_code = status.HTTP_404_NOT_FOUND
        resulted_status_code = response.status_code
        msg = "Verify if the status code is 404 when trying to update a user with invalid id"
        self.assertEqual(expected_status_code, resulted_status_code, msg=msg)

        expected_response = {"detail": "Not found."}
        resulted_response = response.data
        msg = "Verify if the response is the expected when trying to update a user with invalid id"
        self.assertEqual(expected_response, resulted_response, msg=msg)

    # Verify if login is successful
    def test_login_is_successful(self):
        user = baker.make(User, type="donor", email="test@mail.com", password="123456")
        user.set_password(user.password)
        user.save()

        with self.subTest("Verify if login is successful with email"):
            url = reverse("login")
            data = {"email": "test@mail.com", "password": "123456"}
            response = self.client.post(url, data)
            # pdb.set_trace()
            expected_status_code = status.HTTP_200_OK
            resulted_status_code = response.status_code
            msg = "Verify if the status code is 200 when trying to login with email"
            self.assertEqual(expected_status_code, resulted_status_code, msg=msg)

        expected_keys = {"token"}
        resulted_keys = set(response.json().keys())
        msg = "Verify if the response has the expected keys when trying to login with email"
        self.assertEqual(expected_keys, resulted_keys, msg=msg)

    # Verify if login is not successful with invalid email
    def test_login_is_not_successful_with_invalid_email(self):
        user = baker.make(User, type="donor", email="test@mail.com", password="123456")
        user.set_password(user.password)
        user.save()

        url = reverse("login")
        data = {"email": "invalid_email@mail.com", "password": "123456"}
        response = self.client.post(url, data)
        expected_status_code = status.HTTP_401_UNAUTHORIZED
        resulted_status_code = response.status_code
        msg = "Verify if the status code is 401 when trying to login with invalid email"
        self.assertEqual(expected_status_code, resulted_status_code, msg=msg)

    # Verify if login is not successful with invalid password
    def test_login_is_not_successful_with_invalid_password(self):
        user = baker.make(User, type="donor", email="test@mail.com", password="123456")
        user.set_password(user.password)
        user.save()

        url = reverse("login")
        data = {"email": "test@mail.com", "password": "invalid_password"}
        response = self.client.post(url, data)
        expected_status_code = status.HTTP_401_UNAUTHORIZED
        resulted_status_code = response.status_code
        msg = "Verify if the status code is 401 when trying to login with invalid password"
        self.assertEqual(expected_status_code, resulted_status_code, msg=msg)
        
    


