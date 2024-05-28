from django.urls import path
from users.api import views

app_name = "users"

urlpatterns = [
    path("register/", views.RegistrationAPIView.as_view(), name="register"),
    path("login/", views.LoginApiView.as_view(), name="login"),
]
