from rest_framework.test import APITestCase
from .models import Classification
from django.urls import reverse
from rest_framework.views import status
from model_bakery import baker
from users.models import User
import ipdb

class ClassificationsViewsTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user_adm = baker.make(User, type="donor", password="123456", isAdm=True)
        cls.user_adm.set_password(cls.user_adm.password)
        cls.user_adm.save()

        cls.user = baker.make(User, type="donor", password="123456", isAdm=False)
        cls.user.set_password(cls.user.password)
        cls.user.save()

    # python manage.py test --verbosity 2
    def test_create_classification(self):
        data_login = {"email": self.user_adm.email, "password": "123456"}
        url_login = reverse("login")
        response_login = self.client.post(url_login, data_login)
        user_token = response_login.data["token"]
        headers = {"HTTP_AUTHORIZATION": f"Bearer {user_token}"}

        url_classfication = reverse("classifications")
        data_classfication = { "name": "Test1" }
        response_classfication = self.client.post(url_classfication, data_classfication, **headers)

        resulted_data = response_classfication.json()
        expected_fields = {"name", "id"}
        returned_fields = set(resulted_data.keys())
        message1 = "Verify if all fields were successfully created"
        self.assertEqual(expected_fields, returned_fields, msg=message1)

        expected_status = status.HTTP_201_CREATED
        resulted_status = response_classfication.status_code
        message2 = "Verify if the classification was created successfully"
        self.assertEqual(expected_status, resulted_status, msg=message2)

    def test_list_classification(self):
        data_login = {"email": self.user_adm.email, "password": "123456"}
        url_login = reverse("login")
        response_login = self.client.post(url_login, data_login)
        user_token = response_login.data["token"]
        headers = {"HTTP_AUTHORIZATION": f"Bearer {user_token}"}

        url_classfication = reverse("classifications")
        data_classfication1 = { "name": "Test1" }
        data_classfication2 = { "name": "Test2" }
        data_classfication3 = { "name": "Test3" }
        self.client.post(url_classfication, data_classfication1, **headers)
        self.client.post(url_classfication, data_classfication2, **headers)
        self.client.post(url_classfication, data_classfication3, **headers)

        response = self.client.get(url_classfication, **headers)
        message = "Virify if get is pulling everything"
        self.assertEqual(len(response.data), 3, msg=message)

    def test_classification_return_with_rigth_name(self):
        data_login = {"email": self.user_adm.email, "password": "123456"}
        url_login = reverse("login")
        response_login = self.client.post(url_login, data_login)
        user_token = response_login.data["token"]
        headers = {"HTTP_AUTHORIZATION": f"Bearer {user_token}"}

        url_classfication = reverse("classifications")
        data_classfication = { "name": "Test1" }
        self.client.post(url_classfication, data_classfication, **headers)

        url_classifications_name = f"/api/classifications/name/Test1/"
        response = self.client.get(url_classifications_name, **headers)
        message = "Verify get is listing with the right name"
        self.assertEqual(response.data["name"], "Test1", msg=message)

        resulted_data = response.json()
        expected_fields = {"name", "id"}
        returned_fields = set(resulted_data.keys())
        message = "Verify if all fields were successfully returned"
        self.assertEqual(expected_fields, returned_fields, msg=message)
    
    def test_classification_name_return_all_fields(self):
        data_login = {"email": self.user_adm.email, "password": "123456"}
        url_login = reverse("login")
        response_login = self.client.post(url_login, data_login)
        user_token = response_login.data["token"]
        headers = {"HTTP_AUTHORIZATION": f"Bearer {user_token}"}

        url_classfication = reverse("classifications")
        data_classfication = { "name": "Test1" }
        self.client.post(url_classfication, data_classfication, **headers)

        url_classifications_name = f"/api/classifications/name/Test1/"
        response = self.client.get(url_classifications_name, **headers)

        resulted_data = response.json()
        expected_fields = {"name", "id"}
        returned_fields = set(resulted_data.keys())
        message = "Verify if all fields were successfully returned"
        self.assertEqual(expected_fields, returned_fields, msg=message)

    def test_patch_return_data_updated(self):
        data_login = {"email": self.user_adm.email, "password": "123456"}
        url_login = reverse("login")
        response_login = self.client.post(url_login, data_login)
        user_token = response_login.data["token"]
        headers = {"HTTP_AUTHORIZATION": f"Bearer {user_token}"}

        url_classifications = reverse("classifications")
        data_classfication1 = { "name": "Test1" }
        response_create = self.client.post(url_classifications, data_classfication1, **headers)

        url_classifications_id = f"/api/classifications/{response_create.data['id']}/"
        data_updated = { "name": "Test Updated" }
        response_updated = self.client.patch(url_classifications_id, data_updated, **headers)
        message = "Verify the classification has been updated"
        self.assertEqual(response_updated.data["name"], data_updated["name"], msg=message)

    def test_patch_return_all_fields(self):
        data_login = {"email": self.user_adm.email, "password": "123456"}
        url_login = reverse("login")
        response_login = self.client.post(url_login, data_login)
        user_token = response_login.data["token"]
        headers = {"HTTP_AUTHORIZATION": f"Bearer {user_token}"}

        url_classifications = reverse("classifications")
        data_classfication = { "name": "Test1" }
        response_create = self.client.post(url_classifications, data_classfication, **headers)

        url_classifications_id = f"/api/classifications/{response_create.data['id']}/"
        data_updated = { "name": "Test Updated" }
        response_updated = self.client.patch(url_classifications_id, data_updated, **headers)
        message = "Verify the classification return all fields"

        resulted_data = response_updated.json()
        expected_fields = {"name", "id"}
        returned_fields = set(resulted_data.keys())
        self.assertEqual(expected_fields, returned_fields, msg=message)

    def test_delete_classification(self):
        data_login = {"email": self.user_adm.email, "password": "123456"}
        url_login = reverse("login")
        response_login = self.client.post(url_login, data_login)
        user_token = response_login.data["token"]
        headers = {"HTTP_AUTHORIZATION": f"Bearer {user_token}"}

        url_classfication = reverse("classifications")
        data_classfication = { "name": "Test1" }
        response_create = self.client.post(url_classfication, data_classfication, **headers)

        url_classifications_id = f"/api/classifications/{response_create.data['id']}/"
        response_deleted = self.client.delete(url_classifications_id, **headers)
        
        expected_status = status.HTTP_204_NO_CONTENT
        resulted_status = response_deleted.status_code
        message = "Verify if the classification was deleted successfully"
        self.assertEqual(expected_status, resulted_status, msg=message)

    def test_name_already_exist(self):
        data_login = {"email": self.user_adm.email, "password": "123456"}
        url_login = reverse("login")
        response_login = self.client.post(url_login, data_login)
        user_token = response_login.data["token"]
        headers = {"HTTP_AUTHORIZATION": f"Bearer {user_token}"}

        url_classfication = reverse("classifications")
        test1 = { "name": "Test1" }
        test2 = { "name": "Test1" }

        self.client.post(url_classfication, test1, **headers)
        response = self.client.post(url_classfication, test2, **headers)

        expected_status = status.HTTP_400_BAD_REQUEST
        resulted_status = response.status_code
        message = "Verify if the name already exist"
        self.assertEqual(expected_status, resulted_status, msg=message)

        expected_response = {"name": ["This field must be unique."]}
        resulted_response = response.data
        message = "Verify if the name already exist"
        self.assertEqual(expected_response, resulted_response, msg=message)

    def test_create_without_authentication(self):

        headers_invalid = {"HTTP_AUTHORIZATION": f"Bearer {'token_invalid'}"}

        url_classfication = reverse("classifications")
        test1 = { "name": "Test1" }

        response_invalid = self.client.post(url_classfication, test1, **headers_invalid)

        expected_response1 = {"detail": "Given token not valid for any token type","code": "token_not_valid","messages": [{"token_class": "AccessToken","token_type": "access","message": "Token is invalid or expired"}]}
        resulted_response1 = response_invalid.data
        message1 = "Verify if the token is invalid"
        self.assertEqual(expected_response1, resulted_response1, msg=message1)

        expected_status = status.HTTP_401_UNAUTHORIZED
        resulted_status = response_invalid.status_code
        message2 = "Verify if the status is equal to 401 Unauthorized"
        self.assertEqual(expected_status, resulted_status, msg=message2)

        headers_empty = {"HTTP_AUTHORIZATION": f"Bearer {''}"}
        response_empty = self.client.post(url_classfication, test1, **headers_empty)

        expected_response2 = {"detail": "Authorization header must contain two space-delimited values","code": "bad_authorization_header"}
        resulted_response2 = response_empty.data
        message3 = "Verify if the token is invalid"
        self.assertEqual(expected_response2, resulted_response2, msg=message3)

        expected_status = status.HTTP_401_UNAUTHORIZED
        resulted_status = response_empty.status_code
        message4 = "Verify if the status is equal to 401 Unauthorized"
        self.assertEqual(expected_status, resulted_status, msg=message4)

    def test_create_without_adm_permissions(self):
        data_login = {"email": self.user.email, "password": "123456"}
        url_login = reverse("login")
        response_login = self.client.post(url_login, data_login)
        user_token = response_login.data["token"]
        headers = {"HTTP_AUTHORIZATION": f"Bearer {user_token}"}

        url_classfication = reverse("classifications")
        data_classfication = { "name": "Test1" }
        response = self.client.post(url_classfication, data_classfication, **headers)

        expected_response = {"detail": "You do not have permission to perform this action."}
        resulted_response = response.data
        message1 = "Verify if non-admin user tries to create a classifications"
        self.assertEqual(expected_response, resulted_response, msg=message1)

        expected_status = status.HTTP_403_FORBIDDEN
        resulted_status = response.status_code
        message2 = "Verify if the status is equal to 403 Forbidden"
        self.assertEqual(expected_status, resulted_status, msg=message2)

    def test_list_without_authentication(self):
        headers_invalid = {"HTTP_AUTHORIZATION": f"Bearer {'token_invalid'}"}

        url_classfication = reverse("classifications")
        test1 = { "name": "Test1" }

        response_invalid = self.client.get(url_classfication, test1, **headers_invalid)

        expected_response1 = {"detail": "Given token not valid for any token type","code": "token_not_valid","messages": [{"token_class": "AccessToken","token_type": "access","message": "Token is invalid or expired"}]}
        resulted_response1 = response_invalid.data
        message1 = "Verify if the token is invalid"
        self.assertEqual(expected_response1, resulted_response1, msg=message1)

        expected_status = status.HTTP_401_UNAUTHORIZED
        resulted_status = response_invalid.status_code
        message2 = "Verify if the status is equal to 401 Unauthorized"
        self.assertEqual(expected_status, resulted_status, msg=message2)

        headers_empty = {"HTTP_AUTHORIZATION": f"Bearer {''}"}
        response_empty = self.client.get(url_classfication, test1, **headers_empty)

        expected_response2 = {"detail": "Authorization header must contain two space-delimited values","code": "bad_authorization_header"}
        resulted_response2 = response_empty.data
        message3 = "Verify if the token is invalid"
        self.assertEqual(expected_response2, resulted_response2, msg=message3)

        expected_status = status.HTTP_401_UNAUTHORIZED
        resulted_status = response_empty.status_code
        message4 = "Verify if the status is equal to 401 Unauthorized"
        self.assertEqual(expected_status, resulted_status, msg=message4)

    def test_patch_without_authentication(self):
        data_login = {"email": self.user_adm.email, "password": "123456"}
        url_login = reverse("login")
        response_login = self.client.post(url_login, data_login)
        user_token = response_login.data["token"]
        headers = {"HTTP_AUTHORIZATION": f"Bearer {user_token}"}

        url_classifications = reverse("classifications")
        data_classfication = { "name": "Test1" }
        response_create = self.client.post(url_classifications, data_classfication, **headers)

        url_classifications_id = f"/api/classifications/{response_create.data['id']}/"
        headers_invalid = {"HTTP_AUTHORIZATION": f"Bearer {'token_invalid'}"}

        response_invalid = self.client.patch(url_classifications_id, {"name": "Test_Invalid"}, **headers_invalid)

        expected_response1 = {"detail": "Given token not valid for any token type","code": "token_not_valid","messages": [{"token_class": "AccessToken","token_type": "access","message": "Token is invalid or expired"}]}
        resulted_response1 = response_invalid.data
        message1 = "Verify if the token is invalid"
        self.assertEqual(expected_response1, resulted_response1, msg=message1)

        expected_status = status.HTTP_401_UNAUTHORIZED
        resulted_status = response_invalid.status_code
        message2 = "Verify if the status is equal to 401 Unauthorized"
        self.assertEqual(expected_status, resulted_status, msg=message2)

        headers_empty = {"HTTP_AUTHORIZATION": f"Bearer {''}"}
        response_empty = self.client.patch(url_classifications_id, {"name": "Test_Invalid"}, **headers_empty)

        expected_response2 = {"detail": "Authorization header must contain two space-delimited values","code": "bad_authorization_header"}
        resulted_response2 = response_empty.data
        message3 = "Verify if the token is invalid"
        self.assertEqual(expected_response2, resulted_response2, msg=message3)

        expected_status = status.HTTP_401_UNAUTHORIZED
        resulted_status = response_empty.status_code
        message4 = "Verify if the status is equal to 401 Unauthorized"
        self.assertEqual(expected_status, resulted_status, msg=message4)

    def test_patch_without_adm_permissions(self):
        data_login = {"email": self.user.email, "password": "123456"}
        url_login = reverse("login")
        response_login = self.client.post(url_login, data_login)
        user_token = response_login.data["token"]
        headers = {"HTTP_AUTHORIZATION": f"Bearer {user_token}"}

        url_classifications_id = f"/api/classifications/b686fd89-ff05-4025-be22-bb83d1111d83/"
        data_classfication = { "name": "Test1" }
        response = self.client.patch(url_classifications_id, data_classfication, **headers)

        expected_response = {"detail": "You do not have permission to perform this action."}
        resulted_response = response.data
        message1 = "Verify if non-admin user tries to create a classifications"
        self.assertEqual(expected_response, resulted_response, msg=message1)

        expected_status = status.HTTP_403_FORBIDDEN
        resulted_status = response.status_code
        message2 = "Verify if the status is equal to 403 Forbidden"
        self.assertEqual(expected_status, resulted_status, msg=message2)
    
    def test_delete_without_authentication(self):
        url_classifications_id = f"/api/classifications/b686fd89-ff05-4025-be22-bb83d1111d83/"
        headers_invalid = {"HTTP_AUTHORIZATION": f"Bearer {'token_invalid'}"}

        response_invalid = self.client.delete(url_classifications_id, **headers_invalid)

        expected_response1 = {"detail": "Given token not valid for any token type","code": "token_not_valid","messages": [{"token_class": "AccessToken","token_type": "access","message": "Token is invalid or expired"}]}
        resulted_response1 = response_invalid.data
        message1 = "Verify if the token is invalid"
        self.assertEqual(expected_response1, resulted_response1, msg=message1)

        expected_status = status.HTTP_401_UNAUTHORIZED
        resulted_status = response_invalid.status_code
        message2 = "Verify if the status is equal to 401 Unauthorized"
        self.assertEqual(expected_status, resulted_status, msg=message2)

        headers_empty = {"HTTP_AUTHORIZATION": f"Bearer {''}"}
        response_empty = self.client.delete(url_classifications_id, {"name": "Test_Invalid"}, **headers_empty)

        expected_response2 = {"detail": "Authorization header must contain two space-delimited values","code": "bad_authorization_header"}
        resulted_response2 = response_empty.data
        message3 = "Verify if the token is invalid"
        self.assertEqual(expected_response2, resulted_response2, msg=message3)

        expected_status = status.HTTP_401_UNAUTHORIZED
        resulted_status = response_empty.status_code
        message4 = "Verify if the status is equal to 401 Unauthorized"
        self.assertEqual(expected_status, resulted_status, msg=message4)

    def test_delete_without_adm_permissions(self):
        data_login = {"email": self.user.email, "password": "123456"}
        url_login = reverse("login")
        response_login = self.client.post(url_login, data_login)
        user_token = response_login.data["token"]
        headers = {"HTTP_AUTHORIZATION": f"Bearer {user_token}"}

        url_classifications_id = f"/api/classifications/b686fd89-ff05-4025-be22-bb83d1111d83/"
        response = self.client.delete(url_classifications_id, **headers)

        expected_response = {"detail": "You do not have permission to perform this action."}
        resulted_response = response.data
        message1 = "Verify if non-admin user tries to create a classifications"
        self.assertEqual(expected_response, resulted_response, msg=message1)

        expected_status = status.HTTP_403_FORBIDDEN
        resulted_status = response.status_code
        message2 = "Verify if the status is equal to 403 Forbidden"
        self.assertEqual(expected_status, resulted_status, msg=message2)
    
    def test_delete_by_invalid_id(self):
        data_login = {"email": self.user_adm.email, "password": "123456"}
        url_login = reverse("login")
        response_login = self.client.post(url_login, data_login)
        user_token = response_login.data["token"]
        headers = {"HTTP_AUTHORIZATION": f"Bearer {user_token}"}

        url_classifications_id = f"/api/classifications/b686fd89-ff05-4025-be22-bb83d1111d83/"
        response = self.client.delete(url_classifications_id, **headers)

        expected_response = {"detail": "Not found."}
        resulted_response = response.data
        message1 = "Verify id not found"
        self.assertEqual(expected_response, resulted_response, msg=message1)

        expected_status = status.HTTP_404_NOT_FOUND
        resulted_status = response.status_code
        message2 = "Verify if the status is equal to 404 Not Found"
        self.assertEqual(expected_status, resulted_status, msg=message2)
    
    def test_patch_by_invalid_id(self):
        data_login = {"email": self.user_adm.email, "password": "123456"}
        url_login = reverse("login")
        response_login = self.client.post(url_login, data_login)
        user_token = response_login.data["token"]
        headers = {"HTTP_AUTHORIZATION": f"Bearer {user_token}"}

        url_classifications_id = f"/api/classifications/b686fd89-ff05-4025-be22-bb83d1111d83/"
        response = self.client.patch(url_classifications_id, **headers)

        expected_response = {"detail": "Not found."}
        resulted_response = response.data
        message1 = "Verify id not found"
        self.assertEqual(expected_response, resulted_response, msg=message1)

        expected_status = status.HTTP_404_NOT_FOUND
        resulted_status = response.status_code
        message2 = "Verify if the status is equal to 404 Not Found"
        self.assertEqual(expected_status, resulted_status, msg=message2)