import pytest

from django.urls import reverse

from helenite_app.models import Profile


def test_keyword_token_authentication(
    client, user_and_token, valid_data_for_user_and_profile
) -> None:
    """
    Tests that the keyword for the token authentication is "Bearer" instead of
    "Token".
    """

    user, token = user_and_token

    valid_data_for_user_and_profile["user"] = user
    Profile.objects.create(**valid_data_for_user_and_profile)

    headers = {"Authorization": f"Bearer {token.key}"}
    response_passed = client.get(reverse("feed_endpoint"), headers=headers)

    wrong_headers = {"Authorization": f"Token {token.key}"}
    response_denied = client.get(reverse("feed_endpoint"), headers=wrong_headers)

    assert response_denied.status_code == 401

    assert response_passed.status_code == 200
    assert response_passed.wsgi_request.user == user
