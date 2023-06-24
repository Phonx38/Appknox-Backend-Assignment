from rest_framework import serializers
from django.utils import timezone
from .models import Event, Ticket
from django.db import transaction

from django.db.models import Sum


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = "__all__"
        read_only_fields = ["created_by"]


class TicketSerializer(serializers.ModelSerializer):
    event = EventSerializer(read_only=True)

    class Meta:
        model = Ticket
        fields = "__all__"
        read_only_fields = ["booking_time"]


class TicketCreateSerializer(serializers.ModelSerializer):
    event = serializers.PrimaryKeyRelatedField(queryset=Event.objects.all())

    class Meta:
        model = Ticket
        fields = "__all__"
        read_only_fields = ("user",)

    def validate(self, attrs):
        event = attrs["event"]
        user = self.context["request"].user
        quantity = attrs.get("quantity", 1)

        # Check if the event's booking window is open
        if not event.booking_start <= timezone.now() <= event.booking_end:
            raise serializers.ValidationError(
                "Booking window for this event is now closed."
            )

        # Check if the user has already booked the maximum number of tickets
        user_booked_tickets = (
            Ticket.objects.filter(event=event, user=user).aggregate(
                total=Sum("quantity")
            )["total"]
            or 0
        )

        # Check if user is trying to book more tickets than allowed per transaction
        if quantity > event.max_tickets_per_user:
            raise serializers.ValidationError(
                f"You cannot book more than {event.max_tickets_per_user} tickets per user."
            )

        # Check if user's total tickets including this transaction exceed maximum allowed
        if user_booked_tickets + quantity > event.max_tickets_per_user:
            raise serializers.ValidationError(
                f"You've already booked {user_booked_tickets} tickets. You cannot book more than {event.max_tickets_per_user} tickets in total for this event."
            )

        with transaction.atomic():
            # Check if the event's max_seats has been reached
            booked_seats = (
                Ticket.objects.select_for_update()
                .filter(event=event)
                .aggregate(total=Sum("quantity"))["total"]
                or 0
            )
            if booked_seats + quantity > event.max_seats:
                raise serializers.ValidationError(
                    "No more seats available for this event."
                )

        return attrs


class EventSummarySerializer(serializers.ModelSerializer):
    total_tickets_booked = serializers.SerializerMethodField()
    unique_ticket_bookers = serializers.SerializerMethodField()
    total_revenue = serializers.SerializerMethodField()
    remaining_seats = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = [
            "id",
            "title",
            "event_type",
            "total_tickets_booked",
            "unique_ticket_bookers",
            "total_revenue",
            "remaining_seats",
            "ticket_cost",
        ]

    def get_total_tickets_booked(self, obj):
        return obj.tickets.count()

    def get_unique_ticket_bookers(self, obj):
        return obj.tickets.values_list("user", flat=True).distinct().count()

    def get_total_revenue(self, obj):
        return obj.tickets.count() * float(obj.ticket_cost)

    def get_remaining_seats(self, obj):
        return obj.max_seats - obj.tickets.count()
