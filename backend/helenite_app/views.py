from django.utils import timezone

from django.db.models import Q
from django.contrib.auth.models import User

from rest_framework import generics, serializers, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token

from helenite_app import client

from helenite_app.models import Profile, Post, Like
from helenite_app.serializers import (
    FeedSerializer,
    NewPostSerializer,
    SinglePostSerializer,
    FeedForSingleProfileSerializer,
    SettingsSerializer,
    UserRegistrationSerializer,
    NewCommentSerializer,
    ProfileSearchSerializer,
)
from helenite_app.authentication import TokenAuthentication
from helenite_app.permissions import TokenAgePermission, IsUserPermission


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
    View dedicated to log out the user.

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
    View dedicated to the registration of new users.

    Inherits from DRF's CreateAPIView to provide a way to create a new account.

    Endpoint URL: /api/v1/register/
    HTTP Methods Allowed: POST
    """

    serializer_class = UserRegistrationSerializer
    http_method_names = ["post", "options"]
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                {"detail": "Account created successfully. Please log-in."},
                status=status.HTTP_201_CREATED,
            )
        return Response({"detail": "Invalid data."}, status=status.HTTP_400_BAD_REQUEST)


class FeedListCreateAPIView(generics.ListCreateAPIView):
    """
    API view to retrieve the feed for a given logged-in user, as well as to create
    a new post.

    Inherits from DRF's ListAPIView, providing an endpoint to fetch a collection
    of posts from friends and the user themselves.

    Endpoint URL: /api/v1/feed/
    HTTP Methods Allowed: GET, POST, PUT
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

    def put(self, request, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        post_slug = request.data.get("post_slug")
        like_owner = request.user

        try:
            post = Post.objects.get(post_slug=post_slug)
        except Post.DoesNotExist:
            return Response(
                {"detail": "Post not found."}, status=status.HTTP_404_NOT_FOUND
            )

        like, created = Like.objects.get_or_create(
            like_owner=like_owner, like_parent_post=post
        )

        if not created:
            like.delete()
            return Response(
                {"detail": "Successfully unliked post."}, status=status.HTTP_200_OK
            )

        return Response(
            {"detail": "Successfully liked post."}, status=status.HTTP_201_CREATED
        )


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


class SearchListView(generics.ListAPIView):
    """
    View dedicated to search both the `Profile` as well as the `Post` indexes.

    Inherits from DRF's ListAPIView to provide a list of profiles or posts that
    match the query and the index provided by the user through the use of the Algolia
    search engine.

    Endpoint URL: /api/v1/search/?q=query+parameters&index=index
    HTTP Methods Allowed: GET
    """

    serializer_class = ProfileSearchSerializer
    permission_classes = [IsAuthenticated, TokenAgePermission]
    authentication_classes = [TokenAuthentication, SessionAuthentication]

    def get_queryset(self):
        query = self.request.GET.get("q")
        index = self.request.GET.get("index", "Helenite_Profile")

        if not query or query == "":
            return Response(
                {"detail": "Query cannot be empty."}, status=status.HTTP_400_BAD_REQUEST
            )
        if not index or index == "":
            return Response(
                {"detail": "Index cannot be empty."}, status=status.HTTP_400_BAD_REQUEST
            )
        if index != "Helenite_Profile" and index != "Helenite_Post":
            return Response(
                {"detail": "Invalid index."}, status=status.HTTP_400_BAD_REQUEST
            )

        results_from_algolia = client.perform_search(query, index)

        if results_from_algolia["hits"] == []:
            return None

        slugs = []
        for hit in results_from_algolia["hits"]:
            endpoint = hit["endpoint"]
            slug = endpoint.split("/")[-2]
            slugs.append(slug)

        queryset = Profile.objects.filter(custom_slug_profile__in=slugs)
        return queryset

    def get(self, request, *args, **kwargs):
        search_results = self.get_queryset()

        if search_results is None:
            return Response(
                {"detail": "Sorry, we couldn't find any matches."},
                status=status.HTTP_204_NO_CONTENT,
            )

        return Response(self.get_serializer(search_results, many=True).data)


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


class ChangeSettingsAPIView(generics.RetrieveUpdateAPIView):
    """
    API view to retrieve and change user settings.

    Inherits from DRF's RetrieveUpdateAPIView, providing an endpoint to fetch the
    settings for a given profile, as well as a way to change them.

    Endpoint URL: /api/v1/profile/<slug:custom_slug_profile>/change-settings/
    HTTP Methods Allowed: GET, PATCH, DELETE
    """

    permission_classes = [IsAuthenticated, IsUserPermission, TokenAgePermission]
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    lookup_field = "custom_slug_profile"
    serializer_class = SettingsSerializer
    queryset = Profile.objects.filter()
    http_method_names = ["get", "patch", "delete", "head", "options"]

    def patch(self, request, custom_slug_profile):
        profile = self.get_object()
        serializer = self.get_serializer(profile, data=request.data, partial=True)

        if serializer.is_valid():
            old_password = serializer.validated_data.get("old_password")
            new_password = serializer.validated_data.get("new_password")
            # User wants to change their password.
            if old_password and new_password:
                if request.user.check_password(old_password):
                    request.user.set_password(new_password)
                    request.user.save()
                    token = Token.objects.get(user=request.user)
                    token.delete()
                    return Response(
                        {
                            "detail": "Password changed successfully. Please log-in again."
                        },
                        status=status.HTTP_200_OK,
                    )
                else:
                    return Response(
                        {"detail": "Incorrect old password"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
            # Changes in other settings.
            serializer.save()

            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, custom_slug_profile):
        profile = self.get_object()
        if request.user == profile.user:
            found_user = User.objects.get(username=profile.user.username)
            found_user.delete()
            return Response(
                {"detail": "Accound successfully deleted."},
                status=status.HTTP_200_OK,
            )

        return Response(
            {"detail": "You don't have permission to perform that action."},
            status=status.HTTP_401_UNAUTHORIZED,
        )


class PostRetriveCreateDeleteAPIView(generics.RetrieveAPIView):
    """
    View to retrieve a single post based on the post_slug. Also allows for commenting
    and deleting the post.

    Inherits from DRF's RetrieveAPIView to provide a single post alongside its
    likes, comments and counts for both. Depending on the HTTP method and permissions,
    also allows deleting.

    Endpoint URL: /api/v1/profile/post/<slug:post_slug>/
    HTTP Methods Allowed: GET, POST, PUT, DELETE
    """

    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated, TokenAgePermission]
    queryset = Post.objects.filter()
    lookup_field = "post_slug"

    def get_serializer_class(self):
        if self.request.method == "POST":
            return NewCommentSerializer
        return SinglePostSerializer

    def create_comment(self, request, post):
        serializer = NewCommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(comment_parent_post=post, comment_user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete_post(self, request, post):
        if post.post_parent_user == request.user:
            post.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            {"detail": "You don't have permission to delete that post."},
            status=status.HTTP_403_FORBIDDEN,
        )

    def get(self, request, post_slug):
        post = self.get_object()
        return Response(self.get_serializer(post).data)

    def post(self, request, post_slug):
        data = request.data
        serializer = NewCommentSerializer(data=data)
        post = self.get_object()

        if serializer.is_valid():
            serializer.save(comment_parent_post=post, comment_user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, post_slug):
        post = self.get_object()
        if request.user == post.post_parent_user:
            self.delete_post(request, post)
            return Response(
                {"detail": "Your post was successfully deleted."},
                status=status.HTTP_200_OK,
            )
        return Response(
            {"detail": "You don't have permission to delete that post."},
            status=status.HTTP_403_FORBIDDEN,
        )

    def put(self, request, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        post_slug = request.data.get("post_slug")
        like_owner = request.user

        try:
            post = Post.objects.get(post_slug=post_slug)
        except Post.DoesNotExist:
            return Response(
                {"detail": "Post not found."}, status=status.HTTP_404_NOT_FOUND
            )

        like, created = Like.objects.get_or_create(
            like_owner=like_owner, like_parent_post=post
        )

        if not created:
            like.delete()
            return Response(
                {"detail": "Successfully unliked post."}, status=status.HTTP_200_OK
            )

        return Response(
            {"detail": "Successfully liked post."}, status=status.HTTP_201_CREATED
        )
