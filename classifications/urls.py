from django.urls import path
from . import views


urlpatterns = [
    path("classifications/name/<str:name>/", views.ClassificationNameView.as_view()),
    path("classifications/", views.ClassificationView.as_view()),
    path("classifications/<str:pk>/", views.ClassificationDetailView.as_view()),
]
