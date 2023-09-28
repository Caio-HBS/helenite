import pytest

from django.db.utils import IntegrityError

from helenite_app.models import Profile


def test_generic_create_new_user_and_profile(valid_data_for_user_and_profile) -> None:
    """
    Tests that a new user and profile can be created successfully.
    """

    Profile.objects.create(**valid_data_for_user_and_profile)

    assert Profile.objects.count() == 1


def test_create_new_user_and_profile_missing_data(
    valid_data_for_user_and_profile,
) -> None:
    """
    Test that creating a new user and profile with missing data fails.
    """

    valid_data_for_user_and_profile.pop("user")

    with pytest.raises(IntegrityError):
        Profile.objects.create(**valid_data_for_user_and_profile)


def test_create_new_user_and_profile_no_slug(valid_data_for_user_and_profile) -> None:
    """
    Tests the functionallity of automatically assigning a slug to a created profile
    if one wasn't provided.
    """

    valid_data_for_user_and_profile.pop("custom_slug_profile")
    Profile.objects.create(**valid_data_for_user_and_profile)

    assert Profile.objects.get(custom_slug_profile="test") is not None


def test_get_full_name(valid_data_for_user_and_profile) -> None:
    """
    Tests the "get_full_name" method inside the ``Profile`` model.
    """

    new_profile = Profile.objects.create(**valid_data_for_user_and_profile)

    assert new_profile.get_full_name() == "John Doe"
