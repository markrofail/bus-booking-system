from rest_framework.permissions import BasePermission
from django.core.exceptions import ObjectDoesNotExist
from .models import Customer


class IsCustomer(BasePermission):
    def has_permission(self, request, view):
        return hasattr(request.user, 'customer')
