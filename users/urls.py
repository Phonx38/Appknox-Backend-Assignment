from django.urls import path
from .views import UserCreateView, AdminCreateView, UserLoginView

urlpatterns = [
    path("register/", UserCreateView.as_view(), name="register"),
    path("register/admin/", AdminCreateView.as_view(), name="admin-register"),
    path("login/", UserLoginView.as_view(), name="login"),
]
