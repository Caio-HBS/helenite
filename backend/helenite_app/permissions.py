from datetime import timedelta
from django.utils import timezone
from rest_framework import permissions
from rest_framework.authtoken.models import Token


class TokenAgePermission(permissions.BasePermission):
    """
    Checks that the token age is less than 7 days.
    """

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            try:
                token = Token.objects.get(user=request.user)
                if (timezone.now() - token.created) > timedelta(days=7):
                    return False

                return True
            except Token.DoesNotExist:
                return False

        return True


class IsUserPermission(permissions.BasePermission):
    """
    Checks that a given object owner is the same as the current user.
    """

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated and request.user == obj.user:
            return True
        return False
    