from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from rest_framework.exceptions import NotAuthenticated
from rest_framework.exceptions import PermissionDenied as RestPermissionDenied
from rest_framework.permissions import BasePermission


class PermissionCheckerMixin:
    permission_classes = [FarjadBasePermission]

    def dispatch(self, request, *args, **kwargs):
        for permission in self.permission_classes:
            try:
                if not permission().has_permission(request, self):
                    raise PermissionDenied
            except NotAuthenticated:
                return login_required(lambda x: None)(request)
            except RestPermissionDenied:
                raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


class FarjadBasePermission(BasePermission):
    login_required = False

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
        elif self.login_required:
            raise NotAuthenticated
        return True


class LoginRequired(FarjadBasePermission):
    login_required = True
