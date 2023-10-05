import pytest

from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User

from helenite_app.models import Profile
from helenite_app.permissions import TokenAgePermission, IsUserPermission
from helenite_app.views import FeedListCreateAPIView, ChangeSettingsAPIView

def test_token_age_permission_less_than_7_days(client, user_and_token) -> None:
    """
    Tests that a token whitin the age limit functions as intended.
    """

    user, token = user_and_token
    permission = TokenAgePermission()

    request = client.get(reverse("feed_endpoint"))
    request.user = user

    assert permission.has_permission(request, FeedListCreateAPIView().as_view())


def test_token_age_permission_more_than_7_days(client, user_and_token) -> None:
    """
    Tests that a token outside the age limit is denied.
    """

    user, token = user_and_token
    token.created = timezone.now() - timezone.timedelta(days=8)
    token.save()

    permission = TokenAgePermission()

    request = client.get(reverse("feed_endpoint"))
    request.user = user

    assert (
        permission.has_permission(request, FeedListCreateAPIView().as_view()) is False
    )


def test_is_user_permission_owner(client, valid_data_for_user_and_profile) -> None:
    """
    Tests that the permition will only be conceded if the object belongs to user.
    """

    obj = Profile.objects.create(**valid_data_for_user_and_profile)
    permission = IsUserPermission()

    request = client.get(
        reverse("change_settings_endpoint", kwargs={"custom_slug_profile": "test"})
    )
    request.user = valid_data_for_user_and_profile["user"]

    assert permission.has_object_permission(
        request, ChangeSettingsAPIView().as_view(), obj
    )


def test_is_user_permission_not_owner(client, valid_data_for_user_and_profile) -> None:
    """
    Tests that the permition will be denied if the object doesn't belong to the user.
    """

    obj = Profile.objects.create(**valid_data_for_user_and_profile)
    second_user = User.objects.create(
        username="test2", email="email2@email.com", password="das312fa"
    )
    valid_data_for_user_and_profile["user"] = second_user

    permission = IsUserPermission()

    request = client.get(
        reverse("change_settings_endpoint", kwargs={"custom_slug_profile": "test"})
    )
    request.user = valid_data_for_user_and_profile["user"]

    assert (
        permission.has_object_permission(
            request, ChangeSettingsAPIView().as_view(), obj
        )
        is False
    )
