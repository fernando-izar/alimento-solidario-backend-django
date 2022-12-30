from django.urls import path
from . import views
from rest_framework_simplejwt import views as jwt_views
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data.pop("refresh")
        data["token"] = data.pop("access")
        return data

class CustomTokenObtainPairView(jwt_views.TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    def get_username_field(self):
        return "email"

urlpatterns = [
    path("login/", CustomTokenObtainPairView.as_view()),
    path("users/", views.UserView.as_view()),
    path("users/", views.SoftDeleteUserView.as_view()),
    path("users/<str:pk>/", views.UserDetailView.as_view()),
    path("users/profile/", views.UserProfileView.as_view()),
    path("users/soft/<str:pk>/", views.UserSoftDeleteView.as_view()),
]
