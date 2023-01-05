from django.urls import path
from . import views

urlpatterns = [
    path("donations/expand/", views.DonationExpandView.as_view()),
    path("donations/user/", views.DonationUserView.as_view()),
    path("donations/", views.DonationView.as_view(), name='donations'),
    path("donations/expand/<pk>/", views.DonationExpandDetailView.as_view()),
    path("donations/<pk>/", views.DonationDetailView.as_view()),
]