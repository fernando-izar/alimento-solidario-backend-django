from django.urls import path
from . import views


""" urlpatterns = [
    path("donations/", views.DonationView.as_view()),
    path("donations/<str:pk>/", views.DonationDetailView.as_view()),
    path("donations/user/", views.DonationUserView.as_view()),
    path("donations/expand/", views.DonationExpandView.as_view()),
    path("donations/expand/<str:pk>/", views.DonationExpandDetailView.as_view()),
] """
urlpatterns = [
    path("donations/", views.DonationView.as_view()),
    path("donations/user/", views.DonationUserView.as_view()),
    path("donations/expand/", views.DonationExpandView.as_view()),
    path("donations/expand/<pk>/", views.DonationExpandDetailView.as_view()),
    path("donations/<pk>/", views.DonationDetailView.as_view()),
    path("donations/user/", views.DonationUserView.as_view()),
]