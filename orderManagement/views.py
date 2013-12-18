from django.contrib.auth.models import User
from rest_framework import generics

from orderManagement.serializers import OrderSerializer, OrderItemSerializer, OrderCreaterSerializer
from orderManagement.models import Order, OrderItem
from orderManagement.permissions import IsUserAndWaiting, IsDestroyAndNotSubmitted
from django.contrib.auth.decorators import login_required
from restaurantManagement.models import Restaurant, MenuItem
from django.shortcuts import render
from userManagement.models import Address



class OrderCreater(generics.CreateAPIView):
    model = Order
    serializer_class = OrderCreaterSerializer
    
    def pre_save(self, obj):
        if isinstance(self.request.user , User):   
            setattr(obj, 'user', self.request.user)
        else:
            setattr(obj, 'user', None)  

class OrderDetail(generics.RetrieveUpdateDestroyAPIView):
    model = Order
    serializer_class = OrderSerializer
    permission_classes = (IsUserAndWaiting,)
    
class OrderItemCreater(generics.CreateAPIView):
    model = OrderItem
    serializer_class = OrderItemSerializer
 
class OrderItemDetail(generics.RetrieveDestroyAPIView):
    model = OrderItem
    serializer_class = OrderItemSerializer
    permission_classes = (IsDestroyAndNotSubmitted,)
    
class OrderUpdate(generics.ListAPIView):
    model = Order
    serializer_class = OrderSerializer
    
    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        queryset = Order.objects.all()
        restaurant = self.request.QUERY_PARAMS.get('restaurant', None)
        date = self.request.QUERY_PARAMS.get('date', None)
        if restaurant is not None:
            queryset = queryset.filter(status=1).filter(restaurant=restaurant)
            if date is not None:
                queryset = queryset.filter(created__gte=date)
        else:
            queryset = queryset.none()
        return queryset

@login_required(login_url='/login/') 
def show_order_history(request):
    username = request.user.username
    orders = {}
    n_of_ongoing_orders = 0
    
    restaurant = get_restaurant_from_ownerId(request.user.id)
    if (restaurant):
        n_of_ongoing_orders = count_ongoing_orders(restaurant.id)
        all_orders = Order.objects.filter(restaurant_id=restaurant.id)
        for order in all_orders:
            try:
                address = Address.objects.filter(user_id=order.user_id)[0]
            except IndexError:
                # default address
                address = None
            if not address:
                address = "Pearse Street, Black House 7 (default)"
            orders[order] = address
    return render(request,'order_history.html',{'username': username, 'orders': orders, 'n_ongoing_orders': n_of_ongoing_orders})

@login_required(login_url='/login/') 
def show_order_notification_panel(request):
    username = request.user.username
    orders = {}
    n_of_ongoing_orders = 0
    
    restaurant = get_restaurant_from_ownerId(request.user.id)
    if (restaurant):
        n_of_ongoing_orders = count_ongoing_orders(restaurant.id)
        waiting_orders = Order.objects.filter(restaurant_id=restaurant.id).filter(status=1)
        for order in waiting_orders:
            try:
                address = Address.objects.filter(user_id=order.user_id)[0]
            except IndexError:
                # default address
                address = None
            if not address:
                address = "Pearse Street, Black House 7 (default)"
            orders[order] = address
    return render(request,'order_notifications.html',{'username': username, 'orders': orders, 'n_ongoing_orders': n_of_ongoing_orders})

@login_required(login_url='/login/') 
def show_ongoing_orders(request):
    username = request.user.username
    orders = {}
    
    restaurant = get_restaurant_from_ownerId(request.user.id)
    if (restaurant):
        ongoing_orders = Order.objects.filter(restaurant_id=restaurant.id).filter(status=2)
        for order in ongoing_orders:
            try:
                address = Address.objects.filter(user_id=order.user_id)
            except IndexError:
                # default address
                address = None
            if not address:
                address = "Pearse Street, Black House 7 (default)"
            orders[order] = address
    return render(request,'order_ongoing.html',{'username': username, 'orders': orders})

@login_required(login_url='/login/') 
def accept_order(request, order_id):
    username = request.user.username
    n_of_ongoing_orders = 0
    menu_items = []
    order = None
    error = ''
    
    restaurant = get_restaurant_from_ownerId(request.user.id)
    if (restaurant):
        if order_id:
            order = Order.objects.get(id=order_id)
            if (order):
                order.status = 2
                order.save()
                
                n_of_ongoing_orders = count_ongoing_orders(restaurant.id)
                
                order_items = OrderItem.objects.filter(order_id=order_id)
                if len(order_items) > 0:
                    for item in order_items:
                        menu_item = MenuItem.objects.get(id=item.menu_item_id)
                        if menu_item:
                            menu_items.append(menu_item)
                else:
                    error = 'This order does not have items associated'
    return render(request,'order_details.html',{'username': username, 'items': menu_items, 'error' : error, 'n_ongoing_orders': n_of_ongoing_orders, 'order': order, 'accepted' : True})

@login_required(login_url='/login/') 
def reject_order(request, order_id):
    username = request.user.username
    n_of_ongoing_orders = 0
    menu_items = []
    order = None
    error = ''
    
    restaurant = get_restaurant_from_ownerId(request.user.id)
    if (restaurant):
        if order_id:
            order = Order.objects.get(id=order_id)
            if (order):
                order.status = 3
                order.save()
                
                n_of_ongoing_orders = count_ongoing_orders(restaurant.id)
                
                order_items = OrderItem.objects.filter(order_id=order_id)
                if len(order_items) > 0:
                    for item in order_items:
                        menu_item = MenuItem.objects.get(id=item.menu_item_id)
                        if menu_item:
                            menu_items.append(menu_item)
                else:
                    error = 'This order does not have items associated'
    return render(request,'order_details.html',{'username': username, 'items': menu_items, 'error' : error, 'n_ongoing_orders': n_of_ongoing_orders, 'order': order, 'rejected' : True})

@login_required(login_url='/login/') 
def show_order_details(request, order_id):
    username = request.user.username
    menu_items = []
    error = ''
    n_of_ongoing_orders = 0
    order = None
    
    if order_id:
        restaurant = get_restaurant_from_ownerId(request.user.id)
        order_items = OrderItem.objects.filter(order_id=order_id)
        order = Order.objects.get(id=order_id)
        if (restaurant):
            n_of_ongoing_orders = count_ongoing_orders(restaurant.id)
            if len(order_items) > 0:
                for item in order_items:
                    menu_item = MenuItem.objects.get(id=item.menu_item_id)
                    if menu_item:
                        menu_items.append(menu_item)
            else:
                error = 'This order does not have items associated'
        else:
            error = 'There is no order with this id'
    return render(request,'order_details.html',{'username': username, 'items': menu_items, 'error' : error, 'n_ongoing_orders': n_of_ongoing_orders, 'order': order})

def get_restaurant_from_ownerId(owner_id):
    try:
        restaurant = Restaurant.objects.filter(owner_id=owner_id)[0]
    except IndexError:
        restaurant = None  
    return restaurant

def count_ongoing_orders(restaurant_id):
    count = 0
    ongoing_orders = Order.objects.filter(restaurant_id=restaurant_id).filter(status=2)
    if ongoing_orders:
        count = len(ongoing_orders)
    return count
