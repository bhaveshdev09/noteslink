from rest_framework import permissions


class IsOwnerOrSharedUser(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        return (obj.owner == request.user) or (request.user in obj.shared_with.all())


# class IsNoteOwner(permissions.BasePermission):  #TODO: Modify this 

#     def has_object_permission(self, request, view, obj):
#         return obj.owner == request.user
