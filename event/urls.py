from django.urls import path
from .views import (
    EventListView,
    EventCreateView,
    EventUpdateView,
    TicketCreateView,
    TicketListView,
    EventSummaryView,
)

urlpatterns = [
    path("", EventListView.as_view(), name="event-list"),
    path("create/", EventCreateView.as_view(), name="event-create"),
    path("<int:pk>/update/", EventUpdateView.as_view(), name="event-update"),
    path("<int:pk>/summary/", EventSummaryView.as_view(), name="event-summary"),
    path("tickets/create/", TicketCreateView.as_view(), name="ticket-create"),
    path("tickets/", TicketListView.as_view(), name="ticket-list"),
]
