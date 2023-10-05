import pytest

from django.utils import timezone
from django.urls import reverse
from django.forms import ValidationError
from django.db.utils import IntegrityError
from django.contrib.auth.models import User

from helenite_app.models import Profile, Post
from helenite_app.permissions import TokenAgePermission, IsUserPermission
from helenite_app.authentication import TokenAuthentication
from helenite_app.views import FeedListCreateAPIView, ChangeSettingsAPIView

# --------------------------------DATABASE--------------------------------------


def test_generic_create_user_and_profile(db, valid_data_for_user_and_profile) -> None:
    """
    Tests that a new user and profile can be created successfully.
    """

    Profile.objects.create(**valid_data_for_user_and_profile)

    assert Profile.objects.count() == 1
    assert Profile.objects.get(first_name="John")


def test_create_user_and_profile_missing_data(
    db, valid_data_for_user_and_profile
) -> None:
    """
    Test that creating a new user and profile with missing data fails.
    """

    valid_data_for_user_and_profile.pop("user")

    with pytest.raises(IntegrityError):
        Profile.objects.create(**valid_data_for_user_and_profile)


def test_create_user_and_profile_no_slug(db, valid_data_for_user_and_profile) -> None:
    """
    Tests the functionallity of automatically assigning a slug to a created profile
    if one wasn't provided.
    """

    valid_data_for_user_and_profile.pop("custom_slug_profile")
    Profile.objects.create(**valid_data_for_user_and_profile)

    assert Profile.objects.get(custom_slug_profile="test")


def test_save_profile_with_taken_slug(db, valid_data_for_user_and_profile) -> None:
    """
    Tests the functionallity of automatically assigning a slug to a created profile
    if one wasn't provided and the custom one was already taken.
    """

    profile_1 = Profile.objects.create(**valid_data_for_user_and_profile)

    new_user_profile_2 = User.objects.create(
        username="test2", email="email@email.com", password="dashjk2dsa2"
    )
    valid_data_for_user_and_profile.pop("custom_slug_profile")
    valid_data_for_user_and_profile["user"] = new_user_profile_2
    profile_2 = Profile.objects.create(**valid_data_for_user_and_profile)

    assert profile_2.custom_slug_profile != profile_1.custom_slug_profile


def test_create_profile_same_user(db, valid_data_for_user_and_profile) -> None:
    """
    Tests the one-to-one relation beetween ``Profile`` and ``User``.
    """

    Profile.objects.create(**valid_data_for_user_and_profile)

    with pytest.raises(IntegrityError):
        Profile.objects.create(**valid_data_for_user_and_profile)


def test_get_full_name(db, valid_data_for_user_and_profile) -> None:
    """
    Tests the "get_full_name" method inside the ``Profile`` model.
    """

    new_profile = Profile.objects.create(**valid_data_for_user_and_profile)

    assert new_profile.get_full_name() == "John Doe"


def test_endpoint_property_for_profile(db, valid_data_for_user_and_profile) -> None:
    """
    Tests the "endpoint" property inside the ``Profile`` model.
    """

    new_profile = Profile.objects.create(**valid_data_for_user_and_profile)

    assert new_profile.endpoint == "/api/v1/profile/test/"


def test_generic_create_post(db, valid_data_for_post) -> None:
    """
    Tests that a new post can be created successfully.
    """

    Post.objects.create(**valid_data_for_post)

    assert Post.objects.count() == 1
    assert Post.objects.get(post_slug="hfjk8y790")


def test_create_post_no_image_no_text(db, valid_data_for_post) -> None:
    """
    Tests that a new post need either some text or an image.
    """

    valid_data_for_post.pop("post_text")
    valid_data_for_post.pop("post_image")

    with pytest.raises(ValidationError):
        Post.objects.create(**valid_data_for_post)


def test_create_post_no_slug(db, valid_data_for_post) -> None:
    """
    Tests the functionallity of automatically assigning a random slug to a newly
    created post.
    """

    valid_data_for_post.pop("post_slug")

    new_post = Post.objects.create(**valid_data_for_post)

    assert Post.objects.count() == 1
    assert new_post.post_slug is not None


def test_create_post_same_slug(db, valid_data_for_post) -> None:
    """
    Tests that two posts can't share a same slug.
    """

    valid_data_for_post.pop("post_slug")
    new_post = Post.objects.create(**valid_data_for_post)
    new_post_slug = new_post.post_slug
    valid_data_for_post["post_slug"] = new_post_slug

    with pytest.raises(IntegrityError):
        Post.objects.create(**valid_data_for_post)


def test_endpoint_property_for_post(db, valid_data_for_post) -> None:
    """
    Tests that two posts can't share a same slug.
    """

    new_post = Post.objects.create(**valid_data_for_post)

    assert new_post.endpoint == f"/api/v1/profile/post/{new_post.post_slug}/"


# --------------------------------SERIALIZERS-----------------------------------


# -------------------------------PERMISSIONS------------------------------------


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


# -----------------------------AUTHENTICATION-----------------------------------


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
