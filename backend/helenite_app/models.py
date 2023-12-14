import random
import string

from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.forms import ValidationError
from django.contrib.auth.models import User


class Profile(models.Model):
    """
    An extension of the ``User`` model provided by Django.

    Attributes:
        user: the standard ``User`` provided by Django;
        pfp: the profile picture (can be empty);
        first_name: first name of the user;
        last_name: last name of the user;
        birthday: birthday of the user;
        birth_place: birth place of the user;
        custom_slug_profile: custom slug for profile. Defaults to slugified username;
        friends: many-to-many field related to itself;
        private_profile: privacy setting to hide profile;
        show_birthday: privacy setting to hide birthday on profile page.
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    pfp = models.ImageField(upload_to="profile_pictures", blank=True, null=True)
    first_name = models.CharField(max_length=15, null=False, blank=False)
    last_name = models.CharField(max_length=15, null=False, blank=False)
    birthday = models.DateField(null=False, blank=False)
    birth_place = models.CharField(max_length=50, null=False, blank=False)
    custom_slug_profile = models.SlugField(
        max_length=15, unique=True, null=True, blank=True
    )
    friends = models.ManyToManyField("self", blank=True)
    private_profile = models.BooleanField(default=False)
    show_birthday = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} (@{self.user.username})"

    def save(self, **kwargs):
        """
        Provides an automatic slug based on username as well as a default profile
        picture.
        """

        if not self.custom_slug_profile:
            try:
                self.custom_slug_profile = slugify(self.user.username)
            except:
                self.custom_slug_profile = slugify(self.user.username) + "".join(
                    random.SystemRandom().choice(string.ascii_uppercase + string.digits)
                    for _ in range(5)
                )

        if not self.pfp:
            self.pfp = "profile_pictures/default_pfp.png"
        super().save(**kwargs)

    def is_public(self) -> bool:
        """
        Returns the opposite of "private_profile" for Algolia search engine
        purposes.
        """

        return not self.private_profile

    def get_full_name(self):
        """
        Returns the full name associated with the profile.
        """

        return f"{self.first_name} {self.last_name}"

    def get_absolute_url(self):
        """
        Returns the absolute URL for the endpoint property.
        """

        return f"{reverse('profile_info_endpoint', kwargs={'custom_slug_profile': self.custom_slug_profile})}"

    @property
    def endpoint(self):
        """
        Returns the absolute URL for the endpoint for the serializer.
        """

        return self.get_absolute_url()


class FriendRequest(models.Model):
    """
    Represents a Friend request object.

    Attributes:
        request_made_by: the ``User`` that created the request;
        request_sent_to: the ``User`` to which the request was sent;
        created_at: the time of creation;
        request_id: the id of the request (created automatically);
        accepted: the status of the request (defaults to False).
    """

    request_made_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="friend_requests_sent"
    )
    request_sent_to = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="friend_requests_received"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    request_id = models.CharField(max_length=5, null=False, blank=False)
    accepted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.request_made_by} -> {self.request_sent_to} (status: {'accepted' if self.accepted else 'pending'})"

    def save(self, **kwargs):
        """
        Provides an semi-unique id for the request.
        """
        if not self.request_id:
            self.request_id = "".join(
                random.choice(string.ascii_letters + string.digits) for _ in range(5)
            )
        super().save(**kwargs)


class Post(models.Model):
    """
    Represents a post object.

    Attributes:
        post_parent_profile: many-to-one relation to ``User`` model;
        post_text: the text content of the post (can be blank);
        post_image: the image content of the post (can be blank);
        post_publication_date: auto generated publication date for post;
        post_slug: slug for post;
        post_likes: many-to-many relation to ``Like`` model.
    """

    post_parent_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="created_posts"
    )
    post_text = models.TextField(max_length=300, blank=True)
    post_image = models.ImageField(upload_to="post_images", blank=True)
    post_publication_date = models.DateTimeField(auto_now_add=True)
    post_slug = models.SlugField(max_length=15, unique=True, null=True, blank=True)
    post_likes = models.ManyToManyField(
        User, through="Like", related_name="liked_posts"
    )

    def __str__(self):
        return f"{self.post_text[:16]}... - by {self.post_parent_user.username}"

    def clean(self):
        """
        Prevents the user from creating a post with no image and no text.
        """
        if not self.post_text and not self.post_image:
            raise ValidationError("A post cannot be empty.")

    def save(self, **kwargs):
        """
        Provides an automatic slug generator for posts based on username and
        random string, as well as guarantees that either an image or a text is
        present on the instance before saving
        """

        if not self.post_text and not self.post_image:
            raise ValidationError("A post cannot be empty.")

        if not self.post_slug:
            self.post_slug = "".join(
                random.SystemRandom().choice(string.ascii_uppercase + string.digits)
                for _ in range(14)
            )
        super().save(**kwargs)

    def get_absolute_url(self):
        """
        Returns the absolute URL for the endpoint property.
        """

        return (
            f"{reverse('single_post_endpoint', kwargs={'post_slug': self.post_slug})}"
        )

    @property
    def endpoint(self):
        """
        Returns the absolute URL for the endpoint for the serializer.
        """

        return self.get_absolute_url()

    def is_public(self) -> bool:
        """
        Returns the opposite of "private_profile" for Algolia search engine
        purposes.
        """

        return not self.post_parent_user.profile.private_profile


class Like(models.Model):
    """
    Represents a like left on a ``Post``.

    Attributes:
        like_owner: the ``User`` who left the like;
        like_parent_post: the ``Post`` to which the like was left.
    """

    like_owner = models.ForeignKey(User, on_delete=models.CASCADE)
    like_parent_post = models.ForeignKey(Post, on_delete=models.CASCADE)

    class Meta:
        unique_together = (
            "like_owner",
            "like_parent_post",
        )

    def __str__(self):
        return f"Liked by: {self.like_owner.username}, in {self.like_parent_post.post_slug}"


class Comment(models.Model):
    """
    Represents the comments that can be left of ``Post``.

    Attributes:
        comment_user: user who made the comment;
        comment_parent_post: post on which the comment was left;
        comment_text: the text content of the comment;
        comment_publication_date: auto generated date-time for when the comment
        was left.
    """

    comment_user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_parent_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment_text = models.TextField(max_length=500, null=False, blank=False)
    comment_publication_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.comment_text[:16]}... - by: {self.comment_user.username}, in {self.comment_parent_post.post_parent_user.username}"

    def save(self, **kwargs):
        if not self.comment_text:
            raise ValidationError("You can't create a comment with no text.")

        super().save(**kwargs)
