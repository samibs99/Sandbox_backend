from django.urls import path
from core import views

urlpatterns = [
    path("login/", views.login_user, name="login_user"),
    path("create_user/", views.create_user, name="create_user"),
]
