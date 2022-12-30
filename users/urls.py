from django.urls import path
from . import views
from rest_framework_simplejwt import views as jwt_views

class CustomTokenObtainPairView(jwt_views.TokenObtainPairView):
    def get_username_field(self):
        return "email"

urlpatterns = [
    path("login/", CustomTokenObtainPairView.as_view()),
    path("users/", views.UserView.as_view()),
    path("users/<str:pk>/", views.UserDetailView.as_view()),
    path("users/profile/", views.UserProfileView.as_view()),
    path("users/soft/<str:pk>/", views.UserSoftDeleteView.as_view()),
]
