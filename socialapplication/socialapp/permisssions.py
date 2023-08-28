from rest_framework.permissions import BasePermission

class IsGroupCreator(BasePermission):
    message = "You are not the creator of this group."

    def has_object_permission(self, request, view, obj):
        print("uo")
        return obj.owner == request.user
