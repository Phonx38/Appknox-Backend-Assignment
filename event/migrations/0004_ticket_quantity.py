# Generated by Django 4.2.2 on 2023-06-24 04:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("event", "0003_event_max_tickets_per_user_event_ticket_cost"),
    ]

    operations = [
        migrations.AddField(
            model_name="ticket",
            name="quantity",
            field=models.PositiveIntegerField(default=1),
        ),
    ]
