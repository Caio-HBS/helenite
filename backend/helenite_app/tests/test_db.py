import pytest

from django.forms import ValidationError
from django.db.utils import IntegrityError

from helenite_app.models import Profile, Post, Like, Comment


def test_generic_create_user_and_profile(db, valid_data_for_user_and_profile) -> None:
    """
    Tests that a new user and profile can be created successfully.
    """

    Profile.objects.create(**valid_data_for_user_and_profile)

    assert Profile.objects.count() == 1


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

    assert Profile.objects.get(custom_slug_profile="test") is not None


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


def test_generic_create_post(db, valid_data_for_post) -> None:
    """
    Tests that a new post can be created successfully.
    """

    Post.objects.create(**valid_data_for_post)

    assert Post.objects.count() == 1


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
