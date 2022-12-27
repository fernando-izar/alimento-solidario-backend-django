from django.urls import path
from . import views


urlpatterns = [
    path("reservations/", views.ReservationView.as_view()),
    path("reservations/<str:pk>/", views.ReservationDetailView.as_view()),
    path("reservations/user/", views.ReservationUserView.as_view()),
]
