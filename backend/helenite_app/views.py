from django.db.models import Q
from django.contrib.auth.models import User

from rest_framework import generics, serializers

from helenite_app.models import Profile, Post, Like, Comment
from helenite_app.serializers import FeedSerializer, NewPostSerializer


class FeedListCreateAPIView(generics.ListCreateAPIView):
    """
    API view to retrieve the feed for a given logged-in user, as well as to create
    a new post.

    Inherits from DRF's ListAPIView, providing an endpoint to fetch a collection 
    of posts from friends and the user themselves.

    Endpoint URL: /api/v1/feed/
    HTTP Methods Allowed: GET, POST
    """
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return NewPostSerializer
        return FeedSerializer

    def get_queryset(self):
        user = self.request.user
        friends = user.profile.friends.all()

        queryset = Post.objects.filter(
            Q(post_parent_user=user) | Q(post_parent_user__profile__in=friends)
        )
        return queryset
    
    def perform_create(self, serializer):
        try:
            get_user = User.objects.get(username=self.request.user)
        except Profile.DoesNotExist:
            raise serializers.ValidationError("Couldn't find this profile")
        
        if not self.request.user.is_staff and get_user.user != self.request.user:
            raise serializers.ValidationError(
                "You don't have permission to perform this action"
            )
        
        serializer.is_valid(raise_exception=True)
        serializer.save(post_parent_user=get_user)


class PostRetriveAPIView(generics.RetrieveAPIView):
    lookup_field = 'post_slug'
    queryset = Post.objects.all()
