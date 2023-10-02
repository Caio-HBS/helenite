from rest_framework import serializers

from helenite_app.models import Profile, Post, Like, Comment

class FeedSerializer(serializers.ModelSerializer):
    post_owner_pk = serializers.CharField(source="post_parent_user.pk", read_only=True)
    post_owner_username = serializers.CharField(source="post_parent_user.username", read_only=True)
    likes = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            "post_owner_username",
            "post_owner_pk",
            "post_publication_date",
            "endpoint",
            "post_text",
            "post_image",
            "likes_count",
            "likes",
        ]
    def get_likes(self, obj):
        likes = obj.post_likes.all()
        return [user.username for user in likes]
    
    def get_likes_count(self, obj):
        return obj.post_likes.count()
    

class NewPostSerializer(serializers.ModelSerializer):
    parent_user = serializers.CharField(source="post_parent_user", read_only=True)
    class Meta:
        model = Post
        fields = [
            "parent_user",
            "post_text",
            "post_image",
        ]
