from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Event(models.Model):
    EVENT_TYPE_CHOICES = (
        ("online", "Online"),
        ("offline", "Offline"),
    )

    event_type = models.CharField(
        max_length=10, choices=EVENT_TYPE_CHOICES, default="online"
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=200)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    max_seats = models.PositiveIntegerField()
    max_tickets_per_user = models.PositiveIntegerField(default=1)
    ticket_cost = models.DecimalField(max_digits=6, decimal_places=2)
    booking_start = models.DateTimeField()
    booking_end = models.DateTimeField()
    created_by = models.ForeignKey(
        User, related_name="events", on_delete=models.CASCADE
    )

    class Meta:
        ordering = ["start_time"]


class Ticket(models.Model):
    user = models.ForeignKey(User, related_name="tickets", on_delete=models.CASCADE)
    event = models.ForeignKey(Event, related_name="tickets", on_delete=models.CASCADE)
    booking_time = models.DateTimeField(auto_now_add=True)
    quantity = models.PositiveIntegerField(default=1)
