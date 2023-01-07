from django.urls import path
from . import views
from rest_framework_simplejwt import views as jwt_views
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.exceptions import AuthenticationFailed
from django.forms import model_to_dict


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data.pop("refresh")
        data["token"] = data.pop("access")

        address_dict = model_to_dict(self.user.address)
        user_dict = model_to_dict(self.user)

        data["user"] = {
            "id": self.user.id,
            "name": user_dict["name"],
            "responsible": user_dict["responsible"],
            "contact": user_dict["contact"],
            "type": user_dict["type"],
            "address": {
                "address": address_dict["address"],
                "complement": address_dict["complement"],
                "city": address_dict["city"],
                "state": address_dict["state"],
                "zipCode": address_dict["zipCode"],
            }
        }
        return data
    
    default_error_messages = {
        "no_active_account": "Incorrect email and/or password",}


class CustomTokenObtainPairView(jwt_views.TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    def get_username_field(self):
        return "email"


urlpatterns = [
    path("login/", CustomTokenObtainPairView.as_view(), name="login"),
    path("users/profile/", views.UserProfileView.as_view()),
    path("users/soft/<str:pk>/", views.UserSoftDeleteView.as_view()),
    path("users/<str:pk>/", views.UserDetailView.as_view()),
    path("users/", views.UserView.as_view(), name="users"),
]
