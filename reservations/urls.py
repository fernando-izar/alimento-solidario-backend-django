from django.urls import path
from . import views


urlpatterns = [
    path("reservations/user/", views.ReservationUserView.as_view()),
    path("reservations/<str:pk>/", views.ReservationDetailView.as_view()),
    path("reservations/donations/<pk>/",views.ReservationCreateView.as_view()),
    path("reservations/", views.ReservationView.as_view()),
]
