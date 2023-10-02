from django.utils import timezone

from django.db.models import Q
from django.contrib.auth.models import User

from rest_framework import generics, serializers, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token

from helenite_app.models import Profile, Post, Like, Comment
from helenite_app.serializers import FeedSerializer, NewPostSerializer
from helenite_app.permissions import TokenAgePermission


class LoginView(ObtainAuthToken):
    """
    View dedicated to providing a token for authentication.

    Inherits from DRF's ObtainAuthToken to provide a token that lasts for up to
    7 days.

    Endpoint URL: /api/v1/login/
    HTTP Methods Allowed:  POST
    """

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        try:
            token = Token.objects.get(user=user)
            time_difference = timezone.now() - token.created
            token_valid_duration = timezone.timedelta(days=7)
        
            if time_difference > token_valid_duration:
                token.delete()
                token = Token.objects.create(user=user)
        
        except Token.DoesNotExist:
            token = Token.objects.create(user=user)

        return Response({'token': token.key})


class LogoutView(APIView):
    """
    View dedicated to loggin out user.

    Inherits from DRF's APIView to provide a way to both logout from the current
    sessions, as well as delete the current token.

    Endpoint URL: /api/v1/logout/
    HTTP Methods Allowed:  POST
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        print(request)
        token = Token.objects.get(user=request.user)
        token.delete()

        return Response({'message': 'Logout successfull.'}, status=status.HTTP_200_OK)


class FeedListCreateAPIView(generics.ListCreateAPIView):
    """
    API view to retrieve the feed for a given logged-in user, as well as to create
    a new post.

    Inherits from DRF's ListAPIView, providing an endpoint to fetch a collection
    of posts from friends and the user themselves.

    Endpoint URL: /api/v1/feed/
    HTTP Methods Allowed: GET, POST
    """

    permission_classes = [IsAuthenticated, TokenAgePermission]

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


class PostRetriveAPIView(generics.RetrieveAPIView):
    lookup_field = "post_slug"
    queryset = Post.objects.all()
