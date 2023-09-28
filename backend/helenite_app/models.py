import random
import string

from django.db import models
from django.utils.text import slugify
from django.forms import ValidationError
from django.contrib.auth.models import User


class Profile(models.Model):
    """
    An exstention of the ``User`` model provided by Django

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
    custom_slug_profile = models.SlugField(max_length=15, unique=True, null=True, blank=True)
    friends = models.ManyToManyField("self", blank=True)
    private_profile = models.BooleanField(default=False)
    show_birthday = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} (@{self.user.username})"

    def save(self, **kwargs):
        """
        Provides an automatic slug based on username.
        """
        if not self.custom_slug_profile:
            self.custom_slug_profile = slugify(self.user.username)
        super().save(**kwargs)

    def get_full_name(self):
        """
        Returns the full name associated with the profile.
        """
        return f"{self.first_name} {self.last_name}"


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
        Guarantees that either an image or a text is present on the instance before
        saving.
        """
        if not self.post_text and not self.post_image:
            raise ValidationError("A post cannot be empty.")

    def save(self, **kwargs):
        """
        Provides an automatic slug generator for posts based on username and
        random string.
        """
        if not self.post_slug:
            self.post_slug = "".join(
                random.SystemRandom().choice(string.ascii_uppercase + string.digits)
                for _ in range(8)
            )
        super().save(**kwargs)


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
