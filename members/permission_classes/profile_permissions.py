from django.shortcuts import get_object_or_404
from rest_framework.permissions import BasePermission

from members.models import Member


class ProfilePermission(BasePermission):
    def has_permission(self, request, view):
        super().has_permission(request, view)
        if request.user.is_authenticated:
            print(request.user)
        return True
