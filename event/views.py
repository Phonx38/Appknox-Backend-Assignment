from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, status
from rest_framework.response import Response

from utils.permissions import IsAdminOrReadOnly
from .models import Event, Ticket

from .serializers import (
    EventSerializer,
    EventSummarySerializer,
    TicketCreateSerializer,
    TicketSerializer,
)

from rest_framework_simplejwt.authentication import JWTAuthentication
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes


@extend_schema(
    description="Get the list of all events.",
)
class EventListView(generics.ListAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer


@extend_schema(
    description="Create a new event.",
    examples=[
        OpenApiExample(
            "Event Creation Example",
            value={
                "event_type": "online",
                "title": "My Cool Event",
                "description": "This is a cool event",
                "location": "Virtual",
                "start_time": "2023-06-26T00:00Z",
                "end_time": "2023-06-26T02:00Z",
                "max_seats": 100,
                "max_tickets_per_user": 2,
                "ticket_cost": "20.00",
                "booking_start": "2023-06-20T00:00Z",
                "booking_end": "2023-06-25T00:00Z",
            },
        ),
    ],
)
class EventCreateView(generics.CreateAPIView):
    permission_classes = [IsAdminOrReadOnly]
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    authentication_classes = [JWTAuthentication]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


@extend_schema(
    description="Update an existing event.",
    examples=[
        OpenApiExample(
            "Event Update Example",
            value={
                "title": "My Updated Event",
                "description": "This is an updated cool event",
            },
        ),
    ],
)
class EventUpdateView(generics.UpdateAPIView):
    permission_classes = [IsAdminOrReadOnly]
    authentication_classes = [JWTAuthentication]
    queryset = Event.objects.all()
    serializer_class = EventSerializer


@extend_schema(
    description="Create a new ticket for an event.",
    examples=[
        OpenApiExample(
            "Ticket Creation Example (quantity is optional)",
            value={"event": 1, "quantity": 2},
        ),
    ],
)
class TicketCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    queryset = Ticket.objects.all()
    serializer_class = TicketCreateSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@extend_schema(
    description="Get the list of tickets for the current user.",
)
class TicketListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    serializer_class = TicketSerializer

    def get_queryset(self):
        return Ticket.objects.filter(user=self.request.user)


@extend_schema(
    description="Get the summary of an event.",
)
class EventSummaryView(generics.RetrieveAPIView):
    permission_classes = [IsAdminOrReadOnly]
    queryset = Event.objects.all()
    serializer_class = EventSummarySerializer
    authentication_classes = [JWTAuthentication]
