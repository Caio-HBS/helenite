import pytest

from django.forms import ValidationError
from django.db.utils import IntegrityError
from django.contrib.auth.models import User

from helenite_app.models import Profile, Post


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
