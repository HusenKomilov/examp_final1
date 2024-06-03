from django.urls import path
from integration import views

urlpatterns = [
    path("", views.BasicLoginView.as_view()),
]
