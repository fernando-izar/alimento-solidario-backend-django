from rest_framework.test import APITestCase
from model_bakery import baker
from rest_framework.views import status
from users.models import User
from classifications.models import *
from reservations.models import *
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractBaseUser
from django.urls import reverse
from donations.models import *
import pdb

# Create your tests here.
class ReservationCreateViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.RESERVATION_URL = "/api/reservations/"
        cls.LOGIN_URL = "/api/login/"
        cls.user_donor = baker.make(User, type="donor", email="kenzinho1@email.com", password="123456", isAdm=True)
        cls.user_donor.set_password(cls.user_donor.password)
        cls.user_donor.save()
        cls.user_charity = baker.make(User, type="charity", email="kenzinho2@email.com", password="123456", isAdm=True)
        cls.user_charity.set_password(cls.user_charity .password)
        cls.user_charity.save()

        cls.classification = baker.make(Classification, name="LaticínioSilvetre2")
        cls.donation = baker.make(Donations)
        cls.donation1 = baker.make(Donations)
        cls.donation2 = baker.make(Donations)
        cls.donation3 = baker.make(Donations)
    
        
    def test_create_reservation(self):
        data_login = {"email": self.user_charity.email, "password": "123456"}
        url_login = reverse("login")
        response_login = self.client.post(url_login, data_login)
        user_token = response_login.data["token"]
        headers = {"HTTP_AUTHORIZATION": f"Bearer {user_token}"}

        url_reservation = reverse("reservation")
        data_reservation = {"donation_id": f'{self.donation.id}'}

        response_reservation = self.client.post(url_reservation, data_reservation, **headers)

        resulted_data = response_reservation.json()
        expected_fields = {"user", "id", "donation", "date"}
        returned_fields = set(resulted_data.keys())
        message1 = "Verify if all fields were successfully created"
        self.assertEqual(expected_fields, returned_fields, msg=message1)

        expected_status = status.HTTP_201_CREATED
        resulted_status = response_reservation.status_code
        message2 = "Verify if the classification was created successfully"
        self.assertEqual(expected_status, resulted_status, msg=message2)


    def test_create_reservation_by_without_authentication(self):
       
        url_reservation = reverse('reservationUser')
        data_reservation = {"donation_id": f'{self.donation.id}'}

        response = self.client.post(url_reservation, data_reservation)

        expected_status_code = status.HTTP_401_UNAUTHORIZED
        resulted_status_code = response.status_code
        msg = "Verify if the status code is 401 when trying to create a reservation without authentication"
        self.assertEqual(expected_status_code, resulted_status_code, msg=msg)

        expected_response = {"detail": "Authentication credentials were not provided."}
        resulted_response = response.data
        msg = "Verify if the response is the expected when trying to create a reservation without authentication"
        self.assertEqual(expected_response, resulted_response, msg=msg)    


    def test_create_reservation_with_id_donation_invalid(self):
        data_login = {"email": self.user_charity.email, "password": "123456"}
        url_login = reverse("login")
        response_login = self.client.post(url_login, data_login)
        user_token = response_login.data["token"]
        headers = {"HTTP_AUTHORIZATION": f"Bearer {user_token}"}


        url_reservation = reverse("reservation")
        data_reservation = {"donation_id": f'21a68e10-248f-4407-a743-1260ff53ca17'}

        response_reservation = self.client.post(url_reservation, data_reservation, **headers)

        resulted_data = response_reservation
        expected_response= {"detail": "Not found."}
        returned_response = resulted_data.data
        message1 = "comparing message returns Not Found"
        self.assertEqual(expected_response, returned_response, msg=message1)

        expected_status = status.HTTP_404_NOT_FOUND
        resulted_status = response_reservation.status_code
        message2 = "comparing status returns 404"
        self.assertEqual(expected_status, resulted_status, msg=message2)


    def test_create_reservation_invalid_authentication(self):
        data_login = {"email": self.user_charity.email, "password": "123456"}
        url_login = reverse("login")
        response_login = self.client.post(url_login, data_login)
        user_token = response_login.data["token"]
        headers_invalid = {"HTTP_AUTHORIZATION": f"Bearer {'token_invalid'}"}

        url_reservation = reverse("reservation")
        data_reservation = {"donation_id": f'{self.donation.id}'}

        self.client.post(url_reservation, data_reservation, **headers_invalid)
        
        response_invalid = self.client.get(url_reservation,**headers_invalid)

        resulted_data = response_invalid
        expected_response= {"detail": "Given token not valid for any token type",
	    "code": "token_not_valid",
	    "messages": [{"token_class": "AccessToken","token_type":        
        "access","message":"Token is invalid or expired"}]
}
        returned_response = resulted_data.data
        message1 = "comparing message returns Authentication"
        self.assertEqual(expected_response, returned_response, msg=message1)

        expected_status = status.HTTP_401_UNAUTHORIZED
        resulted_status = response_invalid.status_code
        message2 = "comparing status returns 401"
        self.assertEqual(expected_status, resulted_status, msg=message2)
    
    

    def test_create_reservation_by_donor(self):
        
        data_login = {"email": self.user_donor.email, "password": "123456"}
        url_login = reverse("login")
        response_login = self.client.post(url_login, data_login)
        user_token = response_login.data["token"]
        headers = {"HTTP_AUTHORIZATION": f"Bearer {user_token}"}


        url_reservation = reverse("reservation")
        data_reservation = {"donation_id": f'{self.donation.id}'}

        response_reservation = self.client.post(url_reservation, data_reservation, **headers)

        resulted_data = response_reservation
        expected_response= {"detail": "You do not have permission to perform this action."}
        returned_response = resulted_data.data
        message1 = "You do not have permission to perform this action."
        self.assertEqual(expected_response, returned_response, msg=message1)

        expected_status = status.HTTP_403_FORBIDDEN
        resulted_status = response_reservation.status_code
        message2 = "comparing status returns 403 forbidden"
        self.assertEqual(expected_status, resulted_status, msg=message2)

    def test_list_reservation(self):
        data_login = {"email": self.user_charity.email, "password": "123456"}
        url_login = reverse("login")
        response_login = self.client.post(url_login, data_login)
        user_token = response_login.data["token"]
        headers = {"HTTP_AUTHORIZATION": f"Bearer {user_token}"}

        url_reservation = reverse('reservation')
        data_reservation1 = {"donation_id": f'{self.donation1.id}'}
        data_reservation2 = {"donation_id": f'{self.donation2.id}'}
        data_reservation3 = {"donation_id": f'{self.donation3.id}'}

        self.client.post(url_reservation, data_reservation1, **headers)
        self.client.post(url_reservation, data_reservation2, **headers)
        self.client.post(url_reservation, data_reservation3, **headers)

        response_reservation_get = self.client.get(url_reservation,**headers)
        
        message = "Verify listing reservation"
        self.assertEqual(len( response_reservation_get.data), 3, msg=message)

    def test_list_reservation_invalid_authentication(self):
        data_login = {"email": self.user_charity.email, "password": "123456"}
        url_login = reverse("login")
        response_login = self.client.post(url_login, data_login)
        user_token = response_login.data["token"]
        headers_invalid = {"HTTP_AUTHORIZATION": f"Bearer {'token_invalid'}"}

        url_reservation = reverse('reservationUser')
        data_reservation1 = {"donation_id": f'{self.donation1.id}'}
        self.client.post(url_reservation, data_reservation1, **headers_invalid)
        
        response_invalid = self.client.get(url_reservation,**headers_invalid)

        resulted_data = response_invalid
        expected_response= {"detail": "Given token not valid for any token type",
	    "code": "token_not_valid",
	    "messages": [{"token_class": "AccessToken","token_type":        
        "access","message":"Token is invalid or expired"}]
}
        returned_response = resulted_data.data
        message1 = "comparing message returns Authentication"
        self.assertEqual(expected_response, returned_response, msg=message1)

        expected_status = status.HTTP_401_UNAUTHORIZED
        resulted_status = response_invalid.status_code
        message2 = "comparing status returns 401"
        self.assertEqual(expected_status, resulted_status, msg=message2)

    def test_list_reservation_by_without_authentication(self):
        reservation = baker.make(Reservations)
        url_reservation = reverse('reservationUser')

        response = self.client.get(url_reservation)

        expected_status_code = status.HTTP_401_UNAUTHORIZED
        resulted_status_code = response.status_code
        msg = "Verify if the status code is 401 when trying to delete a donation without authentication"
        self.assertEqual(expected_status_code, resulted_status_code, msg=msg)

        expected_response = {"detail": "Authentication credentials were not provided."}
        resulted_response = response.data
        msg = "Verify if the response is the expected when trying to delete a donation without authentication"
        self.assertEqual(expected_response, resulted_response, msg=msg)
    
        

    def test_cannot_delete_reservation_by_id_without_authentication(self):
        reservation = baker.make(Reservations)
        url = f"{self.RESERVATION_URL}{reservation.id}/"

        response = self.client.delete(url)

        expected_status_code = status.HTTP_401_UNAUTHORIZED
        resulted_status_code = response.status_code
        msg = "Verify if the status code is 401 when trying to delete a donation without authentication"
        self.assertEqual(expected_status_code, resulted_status_code, msg=msg)

        expected_response = {"detail": "Authentication credentials were not provided."}
        resulted_response = response.data
        msg = "Verify if the response is the expected when trying to delete a donation without authentication"
        self.assertEqual(expected_response, resulted_response, msg=msg)

    def test_delete_reservation(self):
        reservation = baker.make(Reservations) 
        url = f'{self.RESERVATION_URL}{reservation.id}/'  

        data_login = {'email': self.user_charity.email, 'password': '123456'}
        url_login = reverse('login')
        response_login = self.client.post(url_login, data_login)
        user_token = response_login.data['token']
        headers = {"HTTP_AUTHORIZATION": f'Bearer {user_token}'}

        response = self.client.delete(url, **headers)

        expected_status_code = status.HTTP_204_NO_CONTENT
        resulted_status_code = response.status_code
        msg = "Verify if the status code is 204 when trying to delete a reservation"
        self.assertEqual(expected_status_code, resulted_status_code, msg=msg)    


    def test_delete_reservation_by_invalid_id(self):
        data_login = {'email': self.user_charity.email, 'password': '123456'}
        url_login = reverse('login')
        response_login = self.client.post(url_login, data_login)
        user_token = response_login.data['token']
        headers = {"HTTP_AUTHORIZATION": f'Bearer {user_token}'}

        url = f"{self.RESERVATION_URL}invalid_id/"
        response = self.client.delete(url, **headers)
        expected_status_code = status.HTTP_404_NOT_FOUND
        resulted_status_code = response.status_code
        msg = "Verify if the status code is 404 when trying to delete a reservation with invalid id"
        self.assertEqual(expected_status_code, resulted_status_code, msg=msg)

        expected_response = {"detail": "Not found."}
        resulted_response = response.data
        msg = "Verify if the response is the expected when trying to delete a reservation with invalid id"
        self.assertEqual(expected_response, resulted_response, msg=msg)    
    

    def test_create_reservation_id_params(self):
        data_login = {"email": self.user_charity.email, "password": "123456"}
        url_login = reverse("login")
        response_login = self.client.post(url_login, data_login)
        user_token = response_login.data["token"]
        headers = {"HTTP_AUTHORIZATION": f"Bearer {user_token}"}

        
        url_reservation = f'{self.RESERVATION_URL}donations/{self.donation.id}/'  
        response_reservation = self.client.post(url_reservation, **headers)

        expected_status_code = status.HTTP_201_CREATED
        resulted_status_code = response_reservation.status_code
        msg = "Verify if the status code is 201 when trying to createa reservation"
        self.assertEqual(expected_status_code, resulted_status_code, msg=msg)  

        resulted_data = response_reservation.json()
        expected_fields = {"user", "id", "donation", "date", "donation_id"}
        returned_fields = set(resulted_data.keys())
        message1 = "Verify if all fields were successfully created"
        self.assertEqual(expected_fields, returned_fields, msg=message1)
          
    def test_create_reservation_id_params_invalid(self):

        data_login = {"email": self.user_charity.email, "password": "123456"}
        url_login = reverse("login")
        response_login = self.client.post(url_login, data_login)
        user_token = response_login.data["token"]
        headers = {"HTTP_AUTHORIZATION": f"Bearer {user_token}"}
        id_donation_invalid = '21a68e10-248f-4407-a743-1260ff53ca17'

        
        url_reservation = f'{self.RESERVATION_URL}donations/{id_donation_invalid}/'  
        response_reservation = self.client.post(url_reservation, **headers)

        resulted_data = response_reservation
        expected_response= {"detail": "Not found."}
        returned_response = resulted_data.data
        message1 = "comparing message returns Not Found"
        self.assertEqual(expected_response, returned_response, msg=message1)

        expected_status = status.HTTP_404_NOT_FOUND
        resulted_status = response_reservation.status_code
        message2 = "comparing status returns 404"
        self.assertEqual(expected_status, resulted_status, msg=message2)


    def test_create_reservation_id_params_without_authentication(self): 
        url_reservation = f'{self.RESERVATION_URL}donations/{self.donation.id}/' 
        response_reservation = self.client.post(url_reservation)

        expected_status_code = status.HTTP_401_UNAUTHORIZED
        resulted_status_code = response_reservation.status_code
        msg = "Verify if the status code is 401 when trying to create a reservation without authentication"
        self.assertEqual(expected_status_code, resulted_status_code, msg=msg)

        expected_response = {"detail": "Authentication credentials were not provided."}
        resulted_response = response_reservation.data
        msg = "Verify if the response is the expected when trying to create a reservation without authentication"
        self.assertEqual(expected_response, resulted_response, msg=msg)    



    
