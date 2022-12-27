from django.urls import path
from . import views
from rest_framework_simplejwt import views as jwt_views


urlpatterns = [
    path("login/", jwt_views.TokenObtainPairView.as_view()),
    path("users/", views.UserView.as_view()),
    path("users/<str:pk>/", views.UserDetailView.as_view()),
    path("users/profile/", views.UserProfileView.as_view()),
    path("users/soft/<str:pk>/", views.UserSoftDeleteView.as_view()),
]
