from rest_framework import serializers, status
from rest_framework.response import Response

from django.contrib.auth.models import User

from helenite_app.models import Profile, Post, Like, Comment


class ProfileSerializer(serializers.ModelSerializer):
    """
    This serializer represents a Profile.

    Fields:
        - user_pk: the ID of the user associated with the profile (read-only);
        - username: the username of the user associated with the profile (read-only);
        - get_full_name: the full associated with the profile;
        - endpoint: the profile's endpoint;
        - pfp: the URL of the user's profile picture.
    """

    user_pk = serializers.CharField(source="user.pk", read_only=True)
    username = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = Profile
        fields = [
            "user_pk",
            "username",
            "get_full_name",
            "endpoint",
            "pfp",
        ]


class FeedSerializer(serializers.ModelSerializer):
    """
    This serializer is responsible for providing the posts for the feed.

    Fields:
        - profile: utilizes the `ProfileSerializer` to provide info related to the user;
        - post_publication_date: publication date for post;
        - endpoint: the endpoint for the post;
        - post_text: the text associated with the post;
        - post_image: the image associated with the post;
        - likes_count: the amount of likes on the post;
        - comments_count: the amount of comments on the post;
        - likes: the usernames of the users who liked the post.
    """

    likes = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()

    profile = ProfileSerializer(source="post_parent_user.profile")

    class Meta:
        model = Post
        fields = [
            "profile",
            "post_publication_date",
            "endpoint",
            "post_text",
            "post_image",
            "likes_count",
            "comments_count",
            "likes",
        ]

    def get_likes(self, obj):
        likes = obj.post_likes.all()
        return [user.username for user in likes]

    def get_likes_count(self, obj):
        return obj.post_likes.count()

    def get_comments_count(self, post):
        comments = Comment.objects.filter(comment_parent_post=post)
        return comments.count()


class FeedWithoutProfileInfoSerializer(FeedSerializer):
    """
    This serializer inherits from `FeedSerializer` and provides the same info,
    but with no profile data they will already be on the post. Used exclusively
    on `FeedForSingleProfileSerializer`.

    Fields:
        - post_publication_date: publication date for post;
        - endpoint: the endpoint for the post;
        - post_text: the text associated with the post;
        - post_image: the image associated with the post;
        - likes_count: the amount of likes on the post;
        - comments_count: the amount of comments on the post;
        - likes: the usernames of the users who liked the post.
    """

    class Meta:
        model = Post
        fields = [
            "post_publication_date",
            "endpoint",
            "post_text",
            "post_image",
            "likes_count",
            "comments_count",
            "likes",
        ]


class FeedForSingleProfileSerializer(ProfileSerializer):
    """
    This serializer is responsible for providing the feed for the single profile
    view, retrieving both profile info, as well as posts made by the user.

    Fields:
        - profile: the profile info;
        - posts: the posts made by the user through `FeedWithoutProfileInfoSerializer` (ready_only);
        - birthday: shows the birthday should the user allow on settings.
    """

    posts = FeedWithoutProfileInfoSerializer(
        many=True, source="user.created_posts", read_only=True
    )
    birthday = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ProfileSerializer.Meta.fields + [
            "birthday",
            "posts",
        ]

    def get_birthday(self, obj):
        if obj.show_birthday:
            return obj.birthday
        return None


class SinglePostSerializer(FeedSerializer):
    """
    This serializer is responsible for providing information for a single profile,
    retrieving both profile info for original poster, as well as comments and likes.

    Fields:
        - profile: the posts made by the user through `ProfileSerializer`;
        - post: the post itself through `FeedSerializer`;
        - comments: the comments left on the post.
    """

    comments = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = FeedSerializer.Meta.fields + ["comments"]

    def get_comments(self, obj):
        comments = Comment.objects.filter(comment_parent_post=obj)
        comment_data = [
            {
                "comment_text": comment.comment_text,
                "comment_user": comment.comment_user.username,
            }
            for comment in comments
        ]
        return comment_data


class NewCommentSerializer(serializers.ModelSerializer):
    """
    This serializer is responsible for a way to comment on a post.
    Fields:
        - comment_text: the text of the comment(may not be blank).
    """

    class Meta:
        model = Comment
        fields = [
            "comment_text",
        ]

    def validate_comment_text(self, value):
        if not value.strip():
            raise serializers.ValidationError("Text commend can't be blank.")
        return value


class NewPostSerializer(serializers.ModelSerializer):
    """
    This serializer is responsible for a way to make a new post.

    Fields:
        - parent_user: the user making the post;
        - post_text: the text for the post (not-required so long as there's as image);
        - post_image: the image associated with the post (not-required so long as there's text).
    """

    parent_user = serializers.CharField(source="post_parent_user", read_only=True)

    class Meta:
        model = Post
        fields = [
            "parent_user",
            "post_text",
            "post_image",
        ]


class SettingsSerializer(serializers.ModelSerializer):
    """
    This serializer is responsible for providing/changing settings associated with
    an account, also allowing for password change and pfp change.

    Fields:
        - pfp: the profile picture for the account;
        - private_profile: private_profile (boolean);
        - show_birthday: show_birthday setting (boolean);
        - old_password: the old password for the account (write-only);
        - new_password: the new password (write-only);
        - confirm_new_password: confirmation for new password (write-only).
    """

    old_password = serializers.CharField(write_only=True, required=False)
    new_password = serializers.CharField(write_only=True, required=False)
    confirm_new_password = serializers.CharField(
        write_only=True,
        required=False,
    )

    class Meta:
        model = Profile
        fields = [
            "pfp",
            "private_profile",
            "show_birthday",
            "old_password",
            "new_password",
            "confirm_new_password",
        ]

    def validate(self, data):
        if data.get("new_password"):
            if data.get("confirm_new_password") == None:
                raise serializers.ValidationError(
                    "Confirmation password wasn't provided"
                )
            elif data.get("old_password") == None:
                raise serializers.ValidationError("Old password wasn't provided")
            elif data.get("new_password") != data.get("confirm_new_password"):
                raise serializers.ValidationError(
                    "Unable to confirm new password. Are they the same?"
                )
            else:
                # TODO: Add password verification.
                pass
        return data


class UserRegistrationSerializer(serializers.Serializer):
    """
    This serializer is responsible for the registration of new users.

    Fields:
        - username: the username chosen by the user (unique);
        - email: the email chosen by the user;
        - password: the password chosen by the user;
        - confirmation_password: confirmation for password;
        - first_name: user's first name;
        - last_name: user's last name;
        - birthday: user's date of birth;
        - birth_place: user's place of birth;
        - show_birthday: hide or show birthday setting (boolean, default=True);
        - custom_slug_profile: chosen slug for profile (not-required);
        - private_profile: make the profile private setting (boolean; default=False).
    """

    username = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, style={"input_type": "password"})
    confirmation_password = serializers.CharField(
        write_only=True, style={"input_type": "password"}
    )
    first_name = serializers.CharField(max_length=15)
    last_name = serializers.CharField(max_length=15)
    birthday = serializers.DateField()
    birth_place = serializers.CharField(max_length=50)
    show_birthday = serializers.BooleanField(default=True)
    custom_slug_profile = serializers.SlugField(max_length=15, required=False)
    private_profile = serializers.BooleanField(default=False)

    def create(self, validated_data):
        # TODO: add extra password validation.
        if validated_data.get("password") != validated_data.get(
            "confirmation_password"
        ):
            raise serializers.ValidationError("Passwords don't correspond.")

        validated_for_user = {}
        validated_for_user["username"] = validated_data.get("username")
        validated_for_user["email"] = validated_data.get("email")
        validated_for_user["password"] = validated_data.get("password")
        new_user = User.objects.create_user(**validated_for_user)

        validated_data.pop("username")
        validated_data.pop("email")
        validated_data.pop("password")
        validated_data.pop("confirmation_password")
        Profile.objects.create(user=new_user, **validated_data)

        return new_user
