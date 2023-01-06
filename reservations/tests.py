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
        cls.user_donor = baker.make(User, type="donor", email="kenzinho1@email.com", password="123456", isAdm=True)
        cls.user_donor.set_password(cls.user_donor.password)
        cls.user_donor.save()
        cls.user_charity = baker.make(User, type="charity", email="kenzinho2@email.com", password="123456", isAdm=True)
        cls.user_charity .set_password(cls.user_charity .password)
        cls.user_charity .save()

        cls.classification = baker.make(Classification, name="Laticínio")
        

    def test_create_reservation(self):
        data_login = {"email": self.user_charity.email, "password": "123456"}
        url_login = reverse("login")
        response_login = self.client.post(url_login, data_login)
        user_token = response_login.data["token"]
        headers = {"HTTP_AUTHORIZATION": f"Bearer {user_token}"}

      

        url_donation = reverse('donations')
        data_donation = {"food": "amoras silvestres", "quantity": "10 caixas", "expiration": "2023-12-12", "classification_id": f'{self.classification.id}'}
        response_donation = self.client.post(url_donation, data_donation, **headers)
        
        

        """ donation = baker.make(Donations,classification=f'{self.classification.id}') """
        
       
        url_reservation = reverse("reservation")
        data_reservation = {"donation_id": response_donation.data["id"]}

        response_reservation = self.client.post(url_reservation, data_reservation, **headers)


        resulted_data = response_reservation.json()
        expected_fields = {"user", "id", "donation", "date", "donation_id"}
        returned_fields = set(resulted_data.keys())
        message1 = "Verify if all fields were successfully created"
        self.assertEqual(expected_fields, returned_fields, msg=message1)

        expected_status = status.HTTP_201_CREATED
        resulted_status = response_reservation.status_code
        message2 = "Verify if the classification was created successfully"
        self.assertEqual(expected_status, resulted_status, msg=message2)

    """  def test_not_create_donor(self):
        
        data_login = {"email": self.user_donor.email, "password": "123456"}
        url_login = reverse("login")
        response_login = self.client.post(url_login, data_login)
        user_token = response_login.data["token"]
        headers = {"HTTP_AUTHORIZATION": f"Bearer {user_token}"}

        donation = baker.make(Donations,classification=f'{self.classification.id}')

        url_reservation = reverse("reservation")
        data_reservation = {"donation": donation.id }

        response_reservation = self.client.post(url_reservation, data_reservation, **headers)

        resulted_data = response_reservation.json()
        expected_fields = {"detail"}
        returned_fields = set(resulted_data.keys())
        message1 = "You do not have permission to perform this action."
        self.assertEqual(expected_fields, returned_fields, msg=message1)

        expected_status = status.HTTP_401_UNAUTHORIZED
        resulted_status = response_reservation.status_code
        message2 = "You do not have permission to perform this action."
        self.assertEqual(expected_status, resulted_status, msg=message2)

    
 """