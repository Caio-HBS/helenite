"""
    test_feed_endpoint
    test_discover_endpoint
    test_retrieve_profile_endpoint
    test_change_settings_endpoint
    test_retrieve_post_endpoint
"""
import pytest

from django.urls import reverse
from django.contrib.auth.models import User

from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token


def test_login_endpoint_success(db) -> None:
    """
    TODO: Add documentation.
    """
    
    user = User.objects.create_user(username="testuser", password="testpassword")

    client = APIClient()

    data = {
        "username": "testuser",
        "password": "testpassword"
    }

    response = client.post(reverse("login_endpoint"), data=data, format='json')
    
    assert response.status_code == 200
    assert "token" in response.data

    token_key = response.data['token']
    token = Token.objects.get(key=token_key)
    assert token.user == user


def test_login_endpoint_fail(db) -> None:
    """
    TODO: Add documentation.
    """

    User.objects.create_user(username='testuser', password='testpassword')

    client = APIClient()

    data = {
        "username": "testuser",
        "password": "wrongpassword"
    }

    response = client.post(reverse("login_endpoint"), data=data, format='json')
    
    assert response.status_code == 400
    assert "non_field_errors" in response.data


def test_logout_endpoint(user_and_token) -> None:
    """
    TODO: Add documentation.
    """

    user, token = user_and_token

    client = APIClient()

    headers = {'Authorization': f"Bearer {token}"}
    response = client.post(reverse("logout_endpoint"), headers=headers)

    assert response.status_code == 200
    assert "message" in response.data
    assert response.data["message"] == "Logout successfull."


def test_register_endpoint_success(db, valid_data_for_register_api) -> None:
    """
    TODO: Add documentation.
    """

    data = valid_data_for_register_api

    client = APIClient()

    response = client.post(reverse("register_new_user"), data=data, format="json")

    assert response.status_code == 201
    assert "detail" in response.data
    assert response.data["detail"] == "Account created successfully. Please log-in."


def test_register_endpoint_fail_password_check(db, valid_data_for_register_api) -> None:
    """
    Tests all the checks on the password while creating a new user.
    """

    client = APIClient()

    valid_data_wrong_password = valid_data_for_register_api
    valid_data_for_register_api["password"] = "dsasd23123"
    valid_data_for_register_api["confirmation_password"] = "dsasd23123ddfddd"

    response_wrong_password = client.post(reverse("register_new_user"), data=valid_data_wrong_password, format="json")

    assert response_wrong_password.status_code == 400
    assert "Passwords don't correspond." in response_wrong_password.data

    invalid_data_length = valid_data_wrong_password
    invalid_data_length["password"] = "das23"
    invalid_data_length["confirmation_password"] = "das23"

    response_length = client.post(reverse("register_new_user"), data=invalid_data_length, format="json")

    assert response_length.status_code == 400
    assert "Password needs to be at least 8 characters long." in response_length.data

    invalid_data_no_letter = valid_data_wrong_password
    invalid_data_no_letter["password"] = "12345678"
    invalid_data_no_letter["confirmation_password"] = "12345678"

    response_no_letter = client.post(reverse("register_new_user"), data=invalid_data_no_letter, format="json")

    assert response_no_letter.status_code == 400
    assert "Password needs to have at least one letter." in response_no_letter.data

    invalid_data_no_number = valid_data_wrong_password
    invalid_data_no_number["password"] = "abcdefgh"
    invalid_data_no_number["confirmation_password"] = "abcdefgh"

    response_no_number = client.post(reverse("register_new_user"), data=invalid_data_no_number, format="json")

    assert response_no_number.status_code == 400
    assert "Password needs to have at least one number." in response_no_number.data


def test_register_endpoint_fail(db, valid_data_for_register_api) -> None:
    """
    TODO: Add documentation.
    """

    data = valid_data_for_register_api
    valid_data_for_register_api.pop("first_name")

    client = APIClient()

    response = client.post(reverse("register_new_user"), data=data, format="json")

    assert response.status_code == 400
    assert "detail" in response.data
    assert response.data["detail"] == "Invalid data."


def test_() -> None:
    """
    TODO: Add documentation.
    """

    pass
