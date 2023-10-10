from algoliasearch_django import AlgoliaIndex
from algoliasearch_django.decorators import register

from helenite_app.models import Profile, Post


@register(Profile)
class ProfileIndex(AlgoliaIndex):
    should_index = "is_public"
    fields = [
        "user", 
        "custom_slug_profile",
        "first_name", 
        "last_name",
        "endpoint"
    ]


@register(Post)
class PostIndex(AlgoliaIndex):
    should_index = "is_public"
    fields = [
        "post_parent_user",
        "post_text",
        "endpoint"
    ]