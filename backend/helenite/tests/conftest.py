import pytest

from django.utils import timezone
from django.contrib.auth.models import User

from rest_framework.authtoken.models import Token

from helenite_app.models import Profile, Post


@pytest.fixture
def create_new_user(
    db, username="test", email="test@email.com", password="dasad232das234"
):
    """
    Creates a new user in the test db.
    """

    new_user = User.objects.create(username=username, email=email, password=password)
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
def create_new_user_and_profile(valid_data_for_user_and_profile):
    """
    Creates a new user in the test db, as well as a profile.
    """

    new_user = User.objects.create(
        username="testt", email="e@mail.com", password="dasasd312423asd"
    )
    valid_data_for_user_and_profile["user"] = new_user
    new_profile = Profile.objects.create(**valid_data_for_user_and_profile)

    return new_user, new_profile


@pytest.fixture
def valid_data_for_post(db, create_new_user):
    """
    Provides valid data for the creation of a new post.
    """

    return {
        "post_parent_user": create_new_user,
        "post_text": "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
        "post_image": "",
        "post_publication_date": "2001-01-01 00:00:00",
        "post_slug": "hfjk8y790",
    }


@pytest.fixture
def valid_data_for_comment(db, create_new_user):
    """
    Provides valid data for the creation of a new comment on a post.
    """

    return {
        "comment_user": create_new_user,
        "comment_parent_post": None,
        "comment_text": "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
        "comment_publication_date": "2001-01-01 00:00:00",
    }


@pytest.fixture
def user_and_token(create_new_user):
    """
    Provides a new user and a token alongside it.
    """

    token = Token.objects.create(
        user=create_new_user, created=timezone.now() - timezone.timedelta(days=6)
    )
    return create_new_user, token

@pytest.fixture
def valid_data_for_register_api():
    return {
        "username": "testuser_api",
        "email": "user@email.com",
        "password": "dsasd23123",
        "confirmation_password": "dsasd23123",
        "first_name": "John",
        "last_name": "Draper",
        "birthday": "2001-07-11",
        "birth_place": "City",
        "show_birthday": True,
        "custom_slug_profile": "tilthbs",
        "private_profile": False
    }
