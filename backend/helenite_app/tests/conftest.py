import pytest

from django.contrib.auth.models import User

from helenite_app.models import Profile


@pytest.fixture
def create_new_user(db):
    """
    Creates a new user in the test db.
    """

    new_user = User.objects.create(
        username="test", email="test@email.com", password="dasad232das234"
    )
    return new_user


@pytest.fixture
def valid_data_for_user_and_profile(db, create_new_user):
    """
    Provides data for the creation of a profile.
    """

    return {
        "user": create_new_user,
        "first_name": "John",
        "last_name": "Doe",
        "birthday": "2001-01-01",
        "birth_place": "United States",
        "custom_slug_profile": "test",
    }


@pytest.fixture
def valid_data_for_post(db, create_new_user):
    return {
        "post_parent_user": create_new_user,
        "post_text": "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
        "post_image": "",
        "post_publication_date": "2001-01-01 00:00:00",
        "post_slug": "hfjk8y790",
    }
