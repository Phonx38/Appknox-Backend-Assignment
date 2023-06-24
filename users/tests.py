import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.mark.django_db
def test_user_create_view(api_client):
    user_data = {
        "username": "testuser",
        "password": "testpassword",
    }
    response = api_client.post(reverse("register"), user_data)
    assert response.status_code == 201
    assert User.objects.count() == 1
    assert User.objects.get().username == "testuser"
    assert User.objects.get().user_type == "user"


@pytest.mark.django_db
def test_admin_create_view(api_client):
    admin_data = {
        "username": "testadmin",
        "password": "testpassword",
    }
    response = api_client.post(reverse("admin-register"), admin_data)
    assert response.status_code == 201
    assert User.objects.count() == 1
    assert User.objects.get().username == "testadmin"
    assert User.objects.get().user_type == "admin"


@pytest.mark.django_db
def test_user_login_view(api_client):
    user_data = {
        "username": "testuser",
        "password": "testpassword",
    }
    User.objects.create_user(**user_data)
    response = api_client.post(
        reverse("login"), {"username": "testuser", "password": "testpassword"}
    )
    assert response.status_code == 200
