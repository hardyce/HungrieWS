from rest_framework import permissions
from orderManagement.models import Order

#Permission for Order
class IsUserAndWaiting(permissions.BasePermission):
    def has_permission(self, request, view, obj=None):
        # Skip the check unless this is an object-level test
        if obj is None:
            return True
        
        # Permissions are only allowed to the owner of the snippet
        if obj.user is not None and (obj.user != request.user):
            return False
        
        ### Users can edit their Order if it is not yet dispatched (status = waiting)
        if (obj.status == 0):
            return True
        else: ###Users can only see their order but not edit if it is already dispatched
            return (request.method in permissions.SAFE_METHODS)
        
#Permission for OrderItem
class IsDestroyAndNotSubmitted(permissions.BasePermission):
    def has_permission(self, request, view, obj=None):
        if obj is None:
            return True
        
        #Users can not delete and order if it has already been submitted
        if obj.order.status != 0:
            return (request.method == 'GET')