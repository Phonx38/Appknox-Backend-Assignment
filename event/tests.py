import pytest

from django.utils import timezone
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_201_CREATED
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Event, Ticket

User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def create_user(db):
    user = User.objects.create(
        username="testuser", password="testpass123", user_type="user"
    )
    return user


@pytest.fixture
def create_admin(db):
    admin = User.objects.create(
        username="testadmin", password="adminpass123", user_type="admin"
    )
    return admin


@pytest.fixture
def create_event(db, create_admin):
    event = Event.objects.create(
        event_type="online",
        title="Test Event",
        description="This is a test event",
        location="Virtual",
        start_time="2023-07-01T00:00Z",
        end_time="2023-07-01T02:00Z",
        max_seats=100,
        max_tickets_per_user=2,
        ticket_cost=20.00,
        booking_start="2023-06-20T00:00Z",
        booking_end="2023-06-30T00:00Z",
        created_by=create_admin,
    )
    return event


@pytest.fixture
def create_ticket(db, create_user, create_event):
    ticket = Ticket.objects.create(
        user=create_user,
        event=create_event,
        quantity=1,
    )
    return ticket


@pytest.mark.django_db
def test_event_list_view(api_client, create_event):
    response = api_client.get(reverse("event-list"))
    assert response.status_code == 200
    assert len(response.json()) == 1


@pytest.mark.django_db
def test_event_create_view(api_client, create_admin):
    token = RefreshToken.for_user(create_admin)
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {token.access_token}")
    event_data = {
        "event_type": "online",
        "title": "Test Event 2",
        "description": "This is another test event",
        "location": "Virtual",
        "start_time": "2023-07-02T00:00Z",
        "end_time": "2023-07-02T02:00Z",
        "max_seats": 100,
        "max_tickets_per_user": 2,
        "ticket_cost": 20.00,
        "booking_start": "2023-06-20T00:00Z",
        "booking_end": "2023-06-30T00:00Z",
    }
    response = api_client.post(reverse("event-create"), event_data)
    assert response.status_code == 201
    assert response.json()["title"] == event_data["title"]


@pytest.mark.django_db
def test_ticket_create_view(api_client, create_user, create_event):
    token = RefreshToken.for_user(create_user)
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {token.access_token}")
    ticket_data = {
        "event": create_event.id,
        "quantity": 1,
    }
    response = api_client.post(reverse("ticket-create"), ticket_data)
    assert response.status_code == 201
    assert response.json()["event"] == ticket_data["event"]


@pytest.mark.django_db
def test_max_seats_validation(api_client, create_user, create_event):
    token = RefreshToken.for_user(create_user)
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {token.access_token}")
    ticket_data = {
        "event": create_event.id,
        "quantity": create_event.max_seats + 1,  # exceeding max_seats
    }
    response = api_client.post(reverse("ticket-create"), ticket_data)
    assert response.status_code == HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_event_summary_view(api_client, create_admin, create_event):
    token = RefreshToken.for_user(create_admin)
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {token.access_token}")
    response = api_client.get(reverse("event-summary", kwargs={"pk": create_event.id}))
    assert response.status_code == 200
    assert response.json()["id"] == create_event.id


@pytest.mark.django_db
def test_booking_time_validation(api_client, create_user, create_event):
    token = RefreshToken.for_user(create_user)
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {token.access_token}")

    # Attempting to book before booking start time
    create_event.booking_start = timezone.now() + timezone.timedelta(days=1)
    create_event.save()

    ticket_data = {
        "event": create_event.id,
        "quantity": 1,
    }
    response = api_client.post(reverse("ticket-create"), ticket_data)
    assert response.status_code == HTTP_400_BAD_REQUEST
