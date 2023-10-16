import pytest

from django.urls import reverse
from django.contrib.auth.models import User

from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token

from helenite_app.models import Profile, Post


def test_login_endpoint_success(db) -> None:
    """
    Tests the login endpoint functionality by providing a valid username and
    password.
    """

    user = User.objects.create_user(username="testuser", password="testpassword")

    client = APIClient()

    data = {"username": "testuser", "password": "testpassword"}

    response = client.post(reverse("login_endpoint"), data=data, format="json")

    assert response.status_code == 200
    assert "token" in response.data

    token_key = response.data["token"]
    token = Token.objects.get(key=token_key)
    assert token.user == user


def test_login_endpoint_fail(db) -> None:
    """
    Tests the login endpoint by providing an invalid password.
    """

    User.objects.create_user(username="testuser", password="testpassword")

    client = APIClient()

    data = {"username": "testuser", "password": "wrongpassword"}

    response = client.post(reverse("login_endpoint"), data=data, format="json")

    assert response.status_code == 400
    assert "non_field_errors" in response.data


def test_logout_endpoint(user_and_token) -> None:
    """
    Tests the logout endpoint functionality.
    """

    user, token = user_and_token

    client = APIClient()

    headers = {"Authorization": f"Bearer {token}"}
    response = client.post(reverse("logout_endpoint"), headers=headers)

    assert response.status_code == 200
    assert "message" in response.data
    assert response.data["message"] == "Logout successfull."


def test_register_endpoint_success(db, valid_data_for_register_api) -> None:
    """
    Tests the register endpoint functionality by providing valid data for the
    creation.
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

    # Unmatched passwords.
    valid_data_wrong_password = valid_data_for_register_api
    valid_data_for_register_api["password"] = "dsasd23123"
    valid_data_for_register_api["confirmation_password"] = "dsasd23123ddfddd"

    response_wrong_password = client.post(
        reverse("register_new_user"), data=valid_data_wrong_password, format="json"
    )

    assert response_wrong_password.status_code == 400
    assert "Passwords don't correspond." in response_wrong_password.data

    # Password is not long enough.
    invalid_data_length = valid_data_wrong_password
    invalid_data_length["password"] = "das23"
    invalid_data_length["confirmation_password"] = "das23"

    response_length = client.post(
        reverse("register_new_user"), data=invalid_data_length, format="json"
    )

    assert response_length.status_code == 400
    assert "Password needs to be at least 8 characters long." in response_length.data

    # Password doesn't have any letters.
    invalid_data_no_letter = valid_data_wrong_password
    invalid_data_no_letter["password"] = "12345678"
    invalid_data_no_letter["confirmation_password"] = "12345678"

    response_no_letter = client.post(
        reverse("register_new_user"), data=invalid_data_no_letter, format="json"
    )

    assert response_no_letter.status_code == 400
    assert "Password needs to have at least one letter." in response_no_letter.data

    # Password doesn't have any numbers.
    invalid_data_no_number = valid_data_wrong_password
    invalid_data_no_number["password"] = "abcdefgh"
    invalid_data_no_number["confirmation_password"] = "abcdefgh"

    response_no_number = client.post(
        reverse("register_new_user"), data=invalid_data_no_number, format="json"
    )

    assert response_no_number.status_code == 400
    assert "Password needs to have at least one number." in response_no_number.data


def test_register_endpoint_fail(db, valid_data_for_register_api) -> None:
    """
    Tests the register endpoint functionality by providing incomplete information.
    """

    data = valid_data_for_register_api
    valid_data_for_register_api.pop("first_name")

    client = APIClient()

    response = client.post(reverse("register_new_user"), data=data, format="json")

    assert response.status_code == 400
    assert "detail" in response.data
    assert response.data["detail"] == "Invalid data."


def test_feed_endpoint_get_method(
    db, user_and_token, valid_data_for_post, valid_data_for_user_and_profile
) -> None:
    """
    Tests the feed endpoint functionality by creating a post and trying to retrieve it.
    """

    user, token = user_and_token
    valid_data_for_user_and_profile["user"] = user
    Profile.objects.create(**valid_data_for_user_and_profile)

    valid_data_for_post["post_parent_user"] = user
    Post.objects.create(**valid_data_for_post)

    client = APIClient()

    headers = {"Authorization": f"Bearer {token}"}
    response = client.get(reverse("feed_endpoint"), headers=headers)

    assert response.status_code == 200
    assert response.data["count"] == 1
    assert response.data["results"] != []


def test_feed_endpoint_get_method_no_results(
    db, user_and_token, valid_data_for_user_and_profile
) -> None:
    """
    Tests that a new account with no friends and no posts will return an empty feed.
    """

    user, token = user_and_token
    valid_data_for_user_and_profile["user"] = user
    Profile.objects.create(**valid_data_for_user_and_profile)

    client = APIClient()

    headers = {"Authorization": f"Bearer {token}"}
    response = client.get(reverse("feed_endpoint"), headers=headers)

    assert response.status_code == 200
    assert response.data["count"] == 0
    assert response.data["results"] == []


def test_feed_endpoint_post_method_success(
    db, user_and_token, valid_data_for_user_and_profile
) -> None:
    """
    Tests the creation of new posts through the feed endpoint.
    """

    user, token = user_and_token
    valid_data_for_user_and_profile["user"] = user
    Profile.objects.create(**valid_data_for_user_and_profile)

    headers = {"Authorization": f"Bearer {token}"}

    # Valid data.
    valid_data = {
        "post_text": "Lorem ipsum dolor sit amet, consectetur adipiscing elit."
    }

    client = APIClient()

    valid_response_post = client.post(
        reverse("feed_endpoint"), headers=headers, data=valid_data, format="json"
    )

    assert valid_response_post.status_code == 201
    assert valid_response_post.data["parent_user"] == user.username
    assert valid_response_post.data["post_text"] == valid_data["post_text"]

    response_for_post = client.get(reverse("feed_endpoint"), headers=headers)

    assert response_for_post.status_code == 200
    assert response_for_post.data["count"] == 1

    # Invalid data
    invalid_data = {}

    invalid_response = client.post(
        reverse("feed_endpoint"), headers=headers, data=invalid_data, format="json"
    )

    assert invalid_response.status_code == 400
    assert "non_field_errors" in invalid_response.data
    assert (
        "You either need an image or some text to create a post."
        in invalid_response.data["non_field_errors"]
    )


def test_feed_endpoint_put_method_success(
    db, user_and_token, valid_data_for_post, valid_data_for_user_and_profile
) -> None:
    """
    Tests the like and unlike functions for the feed endpoint.
    """

    user, token = user_and_token
    valid_data_for_user_and_profile["user"] = user
    Profile.objects.create(**valid_data_for_user_and_profile)

    valid_data_for_post["post_parent_user"] = user
    new_post = Post.objects.create(**valid_data_for_post)
    slug = new_post.post_slug

    client = APIClient()

    headers = {"Authorization": f"Bearer {token}"}

    data = {"post_slug": slug}

    # Like a post.
    response_like = client.put(
        reverse("feed_endpoint"), headers=headers, data=data, format="json"
    )

    assert response_like.status_code == 201
    assert response_like.data["detail"] == "Successfully liked post."

    # Unlike a post.
    response_unlike = client.put(
        reverse("feed_endpoint"), headers=headers, data=data, format="json"
    )

    assert response_unlike.status_code == 200
    assert response_unlike.data["detail"] == "Successfully unliked post."


def test_discover_endoint_success(
    db, user_and_token, valid_data_for_post, valid_data_for_user_and_profile
) -> None:
    """
    Tests the discover endpoint functionality
    """

    user1, token = user_and_token
    valid_data_for_user_and_profile["user"] = user1
    Profile.objects.create(**valid_data_for_user_and_profile)

    user2 = User.objects.create(username="test2", password="3213asd312ads")
    valid_data_for_user_and_profile["user"] = user2
    valid_data_for_user_and_profile["custom_slug_profile"] = "test2user"
    Profile.objects.create(**valid_data_for_user_and_profile)

    valid_data_for_post["post_parent_user"] = user2
    new_post = Post.objects.create(**valid_data_for_post)

    client = APIClient()

    headers = {"Authorization": f"Bearer {token}"}

    response = client.get(reverse("discover_endpoint"), headers=headers)

    assert response.status_code == 200
    assert response.data["count"] == 1
    assert response.data["results"] != []


def test_profile_endpoint(
    db, user_and_token, valid_data_for_post, valid_data_for_user_and_profile
) -> None:
    """
    Tests the single profile retrieval functionality.
    """

    user, token = user_and_token
    valid_data_for_user_and_profile["user"] = user
    Profile.objects.create(**valid_data_for_user_and_profile)

    valid_data_for_post["post_parent_user"] = user
    Post.objects.create(**valid_data_for_post)

    client = APIClient()

    headers = {"Authorization": f"Bearer {token}"}

    valid_response = client.get(
        reverse("profile_info_endpoint", kwargs={"custom_slug_profile": "test"}),
        headers=headers,
    )

    assert valid_response.status_code == 200
    assert valid_response.data["username"] == "test"
    assert "test" in valid_response.data["endpoint"]
    assert len(valid_response.data["posts"]) == 1

    invalid_response = client.get(
        reverse("profile_info_endpoint", kwargs={"custom_slug_profile": "invalid"}),
        headers=headers,
    )

    assert invalid_response.status_code == 404
    assert "Not found." in invalid_response.data["detail"]


def test_change_settings_endpoint(
    db, user_and_token, valid_data_for_user_and_profile
) -> None:
    """
    Tests both the change pfp functionality as well as the the change settings in
    the endpoint by providing the necessary info.
    """

    user, token = user_and_token
    valid_data_for_user_and_profile["user"] = user
    new_profile = Profile.objects.create(**valid_data_for_user_and_profile)
    slug = new_profile.custom_slug_profile

    # Test GET.
    headers = {"Authorization": f"Bearer {token}"}
    client = APIClient()

    response_get = client.get(
        reverse("change_settings_endpoint", kwargs={"custom_slug_profile": slug}),
        headers=headers,
    )

    assert response_get.status_code == 200

    # Test PATCH other settings.
    data = {
        "pfp": open("helenite/tests/test_image.png", "rb"),
        "private_profile": True,
        "show_birthday": False,
    }

    response_patch = client.patch(
        reverse("change_settings_endpoint", kwargs={"custom_slug_profile": slug}),
        headers=headers,
        data=data,
        format="multipart",
    )

    assert response_patch.status_code == 200
    assert (
        response_patch.data["private_profile"] == True
        and response_patch.data["show_birthday"] == False
    )
    assert "test_image" in response_patch.data["pfp"]


# def test_change_settings_endpoint_new_password(
#     db, user_and_token, valid_data_for_user_and_profile
# ) -> None:
#     """
#     TODO: Add documentation
#     """

#     user, token = user_and_token
#     valid_data_for_user_and_profile["user"] = user
#     new_profile = Profile.objects.create(**valid_data_for_user_and_profile)
#     slug = new_profile.custom_slug_profile

#     headers = {"Authorization": f"Bearer {token}"}
#     client = APIClient()

#     data = {
#         "old_password": "dasad232das234",
#         "new_password": "ddjkp23231",
#         "confirm_new_password": "ddjkp23231"
#     }

#     valid_response = client.patch(reverse("change_settings_endpoint", kwargs={"custom_slug_profile": slug}), headers=headers, data=data, format="json")

#     print(valid_response.data)
#     print(valid_response.status_code)


def test_delete_account_change_settings_endpoint(
    db, user_and_token, valid_data_for_user_and_profile
) -> None:
    """
    Tests the delete account functionality on the profile settings endpoint.
    """

    user, token = user_and_token
    valid_data_for_user_and_profile["user"] = user
    new_profile = Profile.objects.create(**valid_data_for_user_and_profile)
    slug = new_profile.custom_slug_profile

    headers = {"Authorization": f"Bearer {token}"}
    client = APIClient()

    response = client.delete(
        reverse("change_settings_endpoint", kwargs={"custom_slug_profile": slug}),
        headers=headers,
    )

    assert response.status_code == 200
    assert response.data["detail"] == "Accound successfully deleted."


def test_retrieve_post_enpoint(
    db, user_and_token, valid_data_for_user_and_profile, valid_data_for_post
) -> None:
    """
    Tests the retrieve single post endpoint basic functionality.
    """

    user, token = user_and_token
    valid_data_for_user_and_profile["user"] = user
    new_profile = Profile.objects.create(**valid_data_for_user_and_profile)

    valid_data_for_post["post_parent_user"] = user
    valid_data_for_post.pop("post_image")
    valid_data_for_post.pop("post_publication_date")
    new_post = Post.objects.create(**valid_data_for_post)

    headers = {"Authorization": f"Bearer {token}"}
    client = APIClient()

    response = client.get(
        reverse(
            "single_post_endpoint",
            kwargs={"post_slug": valid_data_for_post["post_slug"]},
        ),
        headers=headers
    )

    assert response.status_code == 200
    assert user.username == response.data["profile"]["username"]
    assert valid_data_for_post["post_text"] == response.data["post_text"]


def test_new_comment_on_post_retrieve_endpoint(
    db, user_and_token, valid_data_for_user_and_profile, valid_data_for_post
) -> None:
    """
    Tests the leave a comment functionality on the single post endpoint.
    """

    user, token = user_and_token
    valid_data_for_user_and_profile["user"] = user
    new_profile = Profile.objects.create(**valid_data_for_user_and_profile)

    valid_data_for_post["post_parent_user"] = user
    valid_data_for_post.pop("post_image")
    valid_data_for_post.pop("post_publication_date")
    new_post = Post.objects.create(**valid_data_for_post)

    headers = {"Authorization": f"Bearer {token}"}
    client = APIClient()
    data = {
        "comment_text": "test comment"
    }

    response = client.post(
        reverse(
            "single_post_endpoint",
            kwargs={"post_slug": valid_data_for_post["post_slug"]},
        ),
        headers=headers, data=data
    )

    assert response.status_code == 201
    assert response.data["comment_text"] == data["comment_text"]


def test_delete_post_on_post_retrieve_endpoint(
    db, user_and_token, valid_data_for_user_and_profile, valid_data_for_post
) -> None:
    """
    Tests the post deletion functionality on the single post endpoint.
    """

    user, token = user_and_token
    valid_data_for_user_and_profile["user"] = user
    new_profile = Profile.objects.create(**valid_data_for_user_and_profile)

    valid_data_for_post["post_parent_user"] = user
    valid_data_for_post.pop("post_image")
    valid_data_for_post.pop("post_publication_date")
    new_post = Post.objects.create(**valid_data_for_post)

    headers = {"Authorization": f"Bearer {token}"}
    client = APIClient()

    response = client.delete(
        reverse(
            "single_post_endpoint",
            kwargs={"post_slug": valid_data_for_post["post_slug"]},
        ),
        headers=headers
    )

    assert response.status_code == 200
    assert response.data["detail"] == "Your post was successfully deleted."


def test_like_post_on_post_retrieve_endpoint(
    db, user_and_token, valid_data_for_user_and_profile, valid_data_for_post
) -> None:
    """
    TODO: Add documentation.
    """

    user, token = user_and_token
    valid_data_for_user_and_profile["user"] = user
    new_profile = Profile.objects.create(**valid_data_for_user_and_profile)

    valid_data_for_post["post_parent_user"] = user
    valid_data_for_post.pop("post_image")
    valid_data_for_post.pop("post_publication_date")
    new_post = Post.objects.create(**valid_data_for_post)

    headers = {"Authorization": f"Bearer {token}"}
    client = APIClient()

    response = client.put(
        reverse(
            "single_post_endpoint",
            kwargs={"post_slug": valid_data_for_post["post_slug"]},
        ),
        headers=headers
    )

    print(response.status_code)
    print(response.data)
