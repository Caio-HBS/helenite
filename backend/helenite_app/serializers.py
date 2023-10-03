from rest_framework import serializers

from helenite_app.models import Profile, Post, Like, Comment


class ProfileSerializer(serializers.ModelSerializer):
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
    

class NewPostSerializer(serializers.ModelSerializer):
    parent_user = serializers.CharField(source="post_parent_user", read_only=True)
    class Meta:
        model = Post
        fields = [
            "parent_user",
            "post_text",
            "post_image",
        ]
