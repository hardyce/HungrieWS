from rest_framework import permissions
from orderManagement.models import Order

class IsUser(permissions.BasePermission):
    def has_permission(self, request, view, obj=None):
        if obj is None:
            return True
        return obj.id == request.user.id


class IsUserURL(permissions.BasePermission):
    def has_permission(self, request, view, obj=None): 
        user_id = int(view.kwargs['user'])
        return user_id == request.user.id
    
class IsAddressUser(permissions.BasePermission):
    def has_permission(self, request, view, obj=None):
        if obj is None:
            return True
        
        if obj.user is None:
            return False
        
        return (obj.user == request.user)