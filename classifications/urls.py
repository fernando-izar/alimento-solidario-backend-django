from django.urls import path
from . import views


urlpatterns = [
    path("classifications/", views.ClassificationView.as_view(), name="classifications"),
    path("classifications/name/<str:name>/", views.ClassificationNameView.as_view()),
    path("classifications/<str:pk>/", views.ClassificationDetailView.as_view()),
]
