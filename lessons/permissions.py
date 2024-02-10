from rest_framework.permissions import BasePermission


class IsModerator(BasePermission):
    massage = "Вы не являетесь модератором"

    def has_permission(self, request, view):
        return request.user.is_staff


class IsOwner(BasePermission):
    massage = "Вы не являетесь владельцем"

    def has_object_permission(self, request, view, obj):
        return request.user == obj.owner
