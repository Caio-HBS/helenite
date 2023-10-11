import pytest

from django.forms import ValidationError
from django.db.utils import IntegrityError
from django.contrib.auth.models import User

from helenite_app.models import Profile, Post, Like, Comment


def test_generic_like(db, create_new_user_and_profile, valid_data_for_post) -> None:
    """
    Tests that a new like on a post can be created successfully.
    """

    valid_data_for_post["post_parent_user"] = create_new_user_and_profile[0]
    new_post = Post.objects.create(**valid_data_for_post)

    Like.objects.create(
        like_owner=create_new_user_and_profile[0], like_parent_post=new_post
    )

    assert Like.objects.count() == 1
    assert Like.objects.get(like_owner=create_new_user_and_profile[0])


def test_one_like_per_user(
    db, create_new_user_and_profile, valid_data_for_post
) -> None:
    """
    Tests that a post can only allow for one like per user.
    """

    valid_data_for_post["post_parent_user"] = create_new_user_and_profile[0]
    new_post = Post.objects.create(**valid_data_for_post)

    Like.objects.create(
        like_owner=create_new_user_and_profile[0], like_parent_post=new_post
    )

    with pytest.raises(IntegrityError):
        Like.objects.create(
            like_owner=create_new_user_and_profile[0], like_parent_post=new_post
        )


def test_unlike(db, create_new_user_and_profile, valid_data_for_post) -> None:
    """
    Tests that a like post can be disliked (deleted).
    """

    valid_data_for_post["post_parent_user"] = create_new_user_and_profile[0]
    new_post = Post.objects.create(**valid_data_for_post)

    Like.objects.create(
        like_owner=create_new_user_and_profile[0], like_parent_post=new_post
    )

    found = Like.objects.get(
        like_owner=create_new_user_and_profile[0], like_parent_post=new_post
    )
    found.delete()

    assert Like.objects.count() == 0
    assert len(Like.objects.filter(like_owner=create_new_user_and_profile[0])) == 0


def test_generic_comment(
    db, valid_data_for_post, valid_data_for_comment, create_new_user_and_profile
) -> None:
    """
    Tests that a new comment can be left on a post.
    """

    valid_data_for_post["post_parent_user"] = create_new_user_and_profile[0]
    new_post = Post.objects.create(**valid_data_for_post)

    valid_data_for_comment["comment_parent_post"] = new_post
    valid_data_for_comment["comment_user"] = create_new_user_and_profile[0]
    Comment.objects.create(**valid_data_for_comment)

    assert Comment.objects.count() == 1
    assert Comment.objects.get(comment_user=create_new_user_and_profile[0])


def test_comment_no_text(
    db, create_new_user_and_profile, valid_data_for_post, valid_data_for_comment
) -> None:
    """
    Tests that a comment can't created without a text.
    """

    valid_data_for_post["post_parent_user"] = create_new_user_and_profile[0]
    new_post = Post.objects.create(**valid_data_for_post)

    valid_data_for_comment.pop("comment_text")
    valid_data_for_comment["comment_parent_post"] = new_post
    valid_data_for_comment["comment_user"] = create_new_user_and_profile[0]

    with pytest.raises(ValidationError):
        Comment.objects.create(**valid_data_for_comment)


def test_multiple_comments_on_same_post(
    db, create_new_user_and_profile, valid_data_for_post, valid_data_for_comment
) -> None:
    """
    Tests that multiple comments can be left on the same post.
    """

    valid_data_for_post["post_parent_user"] = create_new_user_and_profile[0]
    new_post = Post.objects.create(**valid_data_for_post)

    valid_data_for_comment["comment_user"] = create_new_user_and_profile[0]
    valid_data_for_comment["comment_parent_post"] = new_post
    Comment.objects.create(**valid_data_for_comment)

    valid_data_for_comment.update({"comment_text": "new text"})
    Comment.objects.create(**valid_data_for_comment)

    assert Comment.objects.count() == 2


def test_delete_comment(
    db, valid_data_for_post, valid_data_for_comment, create_new_user_and_profile
) -> None:
    """
    Tests that a given comment can be deleted.
    """

    valid_data_for_post["post_parent_user"] = create_new_user_and_profile[0]
    new_post = Post.objects.create(**valid_data_for_post)

    valid_data_for_comment["comment_parent_post"] = new_post
    valid_data_for_comment["comment_user"] = create_new_user_and_profile[0]
    Comment.objects.create(**valid_data_for_comment)

    found = Comment.objects.filter(
        comment_user=create_new_user_and_profile[0].id, comment_parent_post=new_post
    )
    found.delete()

    assert Comment.objects.count() == 0
    assert len(Comment.objects.filter(comment_parent_post=new_post)) == 0


def test_generic_new_friend(
    db, create_new_user, valid_data_for_user_and_profile
) -> None:
    """
    Tests that two users can be friends.
    """

    user1 = Profile.objects.create(**valid_data_for_user_and_profile)

    new_user_2 = User.objects.create(
        username="test2", email="email@myemail.com", password="dfhsjkalf6789"
    )
    valid_data_for_user_and_profile["user"] = new_user_2
    valid_data_for_user_and_profile["custom_slug_profile"] = "test2"
    user2 = Profile.objects.create(**valid_data_for_user_and_profile)

    user2.friends.add(user1)

    assert Profile.objects.count() == 2
    assert user1 in user2.friends.all()


def test_multiple_friends(db, create_new_user, valid_data_for_user_and_profile) -> None:
    """
    Tests that a user can have multiple friends.
    """
    user1 = Profile.objects.create(**valid_data_for_user_and_profile)

    friends = []

    new_user_2 = User.objects.create(
        username="test2", email="email@myemail.com", password="dfhsjkalf6789"
    )
    valid_data_for_user_and_profile["user"] = new_user_2
    valid_data_for_user_and_profile["custom_slug_profile"] = "test2"
    friends.append(Profile.objects.create(**valid_data_for_user_and_profile))

    new_user_3 = User.objects.create(
        username="test3", email="email@myemail.com", password="dfhsjkalf6789"
    )
    valid_data_for_user_and_profile["user"] = new_user_3
    valid_data_for_user_and_profile["custom_slug_profile"] = "test3"
    friends.append(Profile.objects.create(**valid_data_for_user_and_profile))

    new_user_4 = User.objects.create(
        username="test4", email="email@myemail.com", password="dfhsjkalf6789"
    )
    valid_data_for_user_and_profile["user"] = new_user_4
    valid_data_for_user_and_profile["custom_slug_profile"] = "test4"
    friends.append(Profile.objects.create(**valid_data_for_user_and_profile))

    for friend in friends:
        user1.friends.add(friend)

    assert Profile.objects.count() == 4
    for friend in friends:
        assert friend in user1.friends.all()


def test_unfriend(db, create_new_user, valid_data_for_user_and_profile) -> None:
    """
    Tests that friend relation can be terminated.
    """

    user1 = Profile.objects.create(**valid_data_for_user_and_profile)

    new_user_2 = User.objects.create(
        username="test2", email="email@myemail.com", password="dfhsjkalf6789"
    )
    valid_data_for_user_and_profile["user"] = new_user_2
    valid_data_for_user_and_profile["custom_slug_profile"] = "test2"
    user2 = Profile.objects.create(**valid_data_for_user_and_profile)

    user2.friends.add(user1)

    assert user1 in user2.friends.all()

    user2.friends.remove(user1)

    assert Profile.objects.count() == 2
    assert user1 not in user2.friends.all()
