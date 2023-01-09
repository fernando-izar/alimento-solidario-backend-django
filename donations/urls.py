from django.urls import path
from . import views

urlpatterns = [
    path("donations/user/", views.DonationUserView.as_view()),
    path("donations/", views.DonationView.as_view(), name="donations"),
    path("donations/<pk>/", views.DonationDetailView.as_view()),
]
