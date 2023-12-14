# Generated by Django 4.2.6 on 2023-12-14 13:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("helenite_app", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="FriendRequest",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("request_id", models.CharField(max_length=5)),
                ("accepted", models.BooleanField(default=False)),
                (
                    "request_made_by",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="friend_requests_sent",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "request_sent_to",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="friend_requests_received",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
