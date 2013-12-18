from rest_framework import serializers
from orderManagement.models import Order, OrderItem
from restaurantManagement.models import MenuItem
from django.contrib.auth.models import User
from userManagement.serializers import AddressSerializer

from rest_framework import permissions


"""
Nested Serializers
"""
class NestedOrderItemSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = OrderItem
        exclude = ('order',)

"""
Serializers
"""
class OrderItemSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = OrderItem
    def validate_order(self, attrs, source):
        order = attrs[source]
        
        #Submitted orders cannot be changed
        if order.status != 0:
            raise serializers.ValidationError("The Order is already submitted - no changes can be made")
       
        #Anonymous Users can not modify orders of authenticated Users
        order = attrs[source]
        if order.user is None:
            return attrs
        elif order.user != self.context['request'].user:
            raise serializers.ValidationError("You can only edit your own Order!")
        return attrs

class OrderCreaterSerializer(serializers.HyperlinkedModelSerializer):
    order_item = NestedOrderItemSerializer(read_only=True, many=True)
    user = serializers.HyperlinkedRelatedField(read_only=True, view_name='user-detail')
    address = serializers.HyperlinkedRelatedField(read_only=True, view_name='address-detail')
    status = serializers.IntegerField(read_only=True)
    class Meta:
        model = Order

class OrderSerializer(serializers.HyperlinkedModelSerializer):
    order_item = NestedOrderItemSerializer(read_only=True, many=True)
    user = serializers.HyperlinkedRelatedField(read_only=True, view_name='user-detail')
    total = serializers.Field(source='total')
    class Meta:
        model = Order
        
    def validate_status(self, attrs, source):
        #Check that the submitted status value is in 0 or 1 (-- user can not set own status to delivered)
        if int(attrs[source]) not in (0,1):
            raise serializers.ValidationError("Status can only be set to 0 or 1 ||| info: 0 = Order is being created | 1 = Customer is waiting for restaurant response | 2 = Order is accepted by restaurant | 3 = Order is declined by restaurant | 4 = Order was successfully delivered")
        
        #A new order is always starts in the create state
        if self.context['request'].method == 'POST':
            attrs[source] = 0
        elif self.context['request'].method == 'PUT':
        #Users can not choose an address from another user
            if isinstance(attrs['address'].user , User) or (isinstance(self.context['request'], User)):
                if self.context['request'].user != attrs['address'].user:
                    raise serializers.ValidationError("Please choose your own address")
            
        return attrs