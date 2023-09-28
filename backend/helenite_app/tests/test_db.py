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


def test_generic_like(db, create_new_user, valid_data_for_post) -> None:
    """
    Tests that a new like on a post can be created successfully.
    """

    new_post = Post.objects.create(**valid_data_for_post)
    Like.objects.create(like_owner=create_new_user, like_parent_post=new_post)

    assert Like.objects.count() == 1
    assert Like.objects.get(like_owner=create_new_user)


def test_one_like_per_user(db, create_new_user, valid_data_for_post) -> None:
    """
    Tests that a post can only allow for one like per user.
    """

    new_post = Post.objects.create(**valid_data_for_post)
    Like.objects.create(like_owner=create_new_user, like_parent_post=new_post)

    with pytest.raises(IntegrityError):
        Like.objects.create(like_owner=create_new_user, like_parent_post=new_post)


def test_generic_comment(
    db, valid_data_for_post, valid_data_for_comment, create_new_user
) -> None:
    """
    Tests that a new comment can be left on a post.
    """

    new_post = Post.objects.create(**valid_data_for_post)
    valid_data_for_comment["comment_parent_post"] = new_post
    Comment.objects.create(**valid_data_for_comment)

    assert Comment.objects.count() == 1
    assert Comment.objects.get(comment_user=create_new_user)


def test_comment_no_text(db, valid_data_for_post, valid_data_for_comment) -> None:
    """
    Tests that a comment can't created without a text.
    """

    new_post = Post.objects.create(**valid_data_for_post)
    valid_data_for_comment.pop("comment_text")
    valid_data_for_comment["comment_parent_post"] = new_post

    with pytest.raises(ValidationError):
        Comment.objects.create(**valid_data_for_comment)


def test_multiple_comments_on_same_post(
    db, valid_data_for_post, valid_data_for_comment
) -> None:
    """
    Tests that multiple comments can be left on the same post.
    """

    new_post = Post.objects.create(**valid_data_for_post)
    valid_data_for_comment["comment_parent_post"] = new_post
    Comment.objects.create(**valid_data_for_comment)

    valid_data_for_comment.update({"comment_text": "new text"})
    Comment.objects.create(**valid_data_for_comment)

    assert Comment.objects.count() == 2
