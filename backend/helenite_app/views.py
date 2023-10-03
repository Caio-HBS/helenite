from django.utils import timezone

from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

from rest_framework import generics, serializers, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token

from helenite_app.models import Profile, Post, Like, Comment
from helenite_app.serializers import (
    FeedSerializer,
    NewPostSerializer,
    SinglePostSerializer,
    FeedForSingleProfileSerializer,
)
from helenite_app.authentication import TokenAuthentication
from helenite_app.permissions import TokenAgePermission


class LoginView(ObtainAuthToken):
    """
    View dedicated to providing a token for authentication.

    Inherits from DRF's ObtainAuthToken to provide a token that lasts for up to
    7 days.

    Endpoint URL: /api/v1/login/
    HTTP Methods Allowed: POST
    """

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        try:
            token = Token.objects.get(user=user)
            time_difference = timezone.now() - token.created
            token_valid_duration = timezone.timedelta(days=7)

            if time_difference > token_valid_duration:
                token.delete()
                token = Token.objects.create(user=user)

        except Token.DoesNotExist:
            token = Token.objects.create(user=user)

        return Response({"token": token.key})


class LogoutView(APIView):
    """
    View dedicated to loggin out user.

    Inherits from DRF's APIView to provide a way to both logout from the current
    sessions, as well as delete the current token.

    Endpoint URL: /api/v1/logout/
    HTTP Methods Allowed: POST
    """

    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request):
        token = Token.objects.get(user=request.user)
        token.delete()

        return Response({"message": "Logout successfull."}, status=status.HTTP_200_OK)


class RegisterCreateAPIView(generics.CreateAPIView):
    """
    TODO: Add documentation.
    """

    pass


class FeedListCreateAPIView(generics.ListCreateAPIView):
    # TODO: Like a comment while on the feed.
    """
    API view to retrieve the feed for a given logged-in user, as well as to create
    a new post.

    Inherits from DRF's ListAPIView, providing an endpoint to fetch a collection
    of posts from friends and the user themselves.

    Endpoint URL: /api/v1/feed/
    HTTP Methods Allowed: GET, POST
    """

    permission_classes = [IsAuthenticated, TokenAgePermission]
    authentication_classes = [TokenAuthentication, SessionAuthentication]

    def get_serializer_class(self):
        if self.request.method == "POST":
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


class DiscoverListAPIView(generics.ListAPIView):
    """
    View dedicated to providing random posts from random users.

    Inherits from DRF's ListAPIView to provide a list of up to 30 random posts to
    the user so long as the post owner haven't made their profile private.

    Endpoint URL: /api/v1/feed/discover/
    HTTP Methods Allowed: GET
    """

    serializer_class = FeedSerializer
    permission_classes = [IsAuthenticated, TokenAgePermission]
    authentication_classes = [TokenAuthentication, SessionAuthentication]

    def get_queryset(self):
        user = self.request.user

        queryset = Post.objects.filter(
            Q(post_parent_user__profile__private_profile=False)
            & ~Q(post_parent_user=user)
        ).order_by("?")[:30]
        return queryset


class ProfileSearchListView(generics.GenericAPIView):
    """
    TODO: Add documentation.
    """
    pass


class ProfileRetriveAPIView(generics.RetrieveAPIView):
    """
    View to retrieve a single profile based on the custom_slug_profile.

    Inherits from DRF's RetrieveAPIView to provide a single profile alongside its
    posts.

    Endpoint URL: /api/v1/profile/<slug:custom_slug_profile>/
    HTTP Methods Allowed: GET
    """

    lookup_field = "custom_slug_profile"
    serializer_class = FeedForSingleProfileSerializer

    def get_queryset(self):
        queryset = Profile.objects.filter()
        return queryset


class ChangeSettingsUpdateAPIView(generics.UpdateAPIView):
    """
    TODO: Add documentation.
    """

    pass


class PostRetriveAPIView(generics.RetrieveAPIView):
    # TODO: Leave a new comment.
    """
    View to retrieve a single post based on the post_slug.

    Inherits from DRF's RetrieveAPIView to provide a single post alongside its
    likes, comments and counts for both.

    Endpoint URL: /api/v1/profile/post/<slug:post_slug>/
    HTTP Methods Allowed: GET
    """

    lookup_field = "post_slug"
    serializer_class = SinglePostSerializer
    permission_classes = [IsAuthenticated, TokenAgePermission]
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    queryset = Post.objects.filter()
