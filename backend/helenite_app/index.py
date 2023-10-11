from algoliasearch_django import AlgoliaIndex
from algoliasearch_django.decorators import register

from helenite_app.models import Profile, Post


@register(Profile)
class ProfileIndex(AlgoliaIndex):
    """
    Algolia index registration for `Profile`.

    Params:
        - should_index: chooses to index or not based on the `Profile` "private_profile"
        param.

    Fields:
        - user: the `User` for that specific profile;
        - custom_slug_profile: the chooses slug for the profile;
        - fist_name: the user's first name;
        - last_name: the user's last name;
        - endpoint: endpoint for that user.
    """

    should_index = "is_public"
    fields = ["user", "custom_slug_profile", "first_name", "last_name", "endpoint"]


@register(Post)
class PostIndex(AlgoliaIndex):
    """
    Algolia index registration for `Post`.

    Params:
        - should_index: chooses to index or not based on the `post_parent_user.Profile`
        "private_profile" param.

    Fields:
        - user: the `User` that owns the post;
        - post_text: the post text associated with that post;
        - endpoint: endpoint for that user.
    """

    should_index = "is_public"
    fields = ["post_parent_user", "post_text", "endpoint"]
