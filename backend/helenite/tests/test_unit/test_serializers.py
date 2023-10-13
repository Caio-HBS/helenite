import pytest

from django.contrib.auth.models import User

from helenite_app.models import Profile, Post, Comment, Like
from helenite_app.serializers import FeedSerializer, SettingsSerializer


def test_feed_serializer(
    db, create_new_user_and_profile, valid_data_for_post, valid_data_for_comment
) -> None:
    """
    Tests that the feed serializer retrieves the right information.
    """

    user, profile = create_new_user_and_profile

    valid_data_for_post["post_parent_user"] = user
    new_post = Post.objects.create(**valid_data_for_post)

    valid_data_for_comment["comment_user"] = user
    valid_data_for_comment["comment_parent_post"] = new_post
    Comment.objects.create(**valid_data_for_comment)

    Like.objects.create(like_owner=user, like_parent_post=new_post)

    serializer = FeedSerializer(new_post)

    serialized_data = serializer.data
    assert serialized_data["profile"]["user_pk"] == str(user.pk)
    assert (
        serialized_data["post_text"]
        == "Lorem ipsum dolor sit amet, consectetur adipiscing elit."
    )
    assert serialized_data["likes_count"] == 1
    assert serialized_data["comments_count"] == 1
    assert user.username in serialized_data["likes"]
