from rest_framework import serializers
#from rest_framework_gis import serializers
from restaurantManagement.serializers import RestaurantSerializer, OpeningHoursSerializer, RestaurantOpeningHoursSerializer, RestaurantMenuSerializer, MenuItemSerializer, MenuSectionSerializer, RestaurantDistanceSerializer
from restaurantManagement.models import Restaurant, RestaurantCategory, MenuSection, MenuItem, OpeningHours, MAX_DELIVERY_RADIUS
from ratingManagement.serializers import RatingSerializer
from ratingManagement.models import Rating
from orderManagement.views import count_ongoing_orders

from rest_framework import generics
from rest_framework import authentication
from rest_framework import permissions

#### Functional API VIew
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

###Geolocation
import django_filters
from django.contrib.gis.geos import *
from django.contrib.gis.measure import Distance # ``D`` is a shortcut for ``Distance``
from django.db.models import F

###Dashboard
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.log import logger
import sys

from django.db.models import Avg

#############################
#############################

def longlat2restaurant_set(latitude, longitude):
    user_point = Point( float(latitude), float(longitude))
    spatial_restaurant_set = Restaurant.objects.filter(location__distance_lte=(  user_point, Distance(km=MAX_DELIVERY_RADIUS))).distance(user_point)
    
    #reduce result set to restaurants within the area
    delivery_radius_set = []
    for restaurant in spatial_restaurant_set:
        if restaurant.distance.km <= restaurant.delivery_radius:
            delivery_radius_set.append(restaurant.id)

    #convert list to queryset
    return spatial_restaurant_set.filter(pk__in=delivery_radius_set)

############################
############################

class CategoryAbbreviationsList(APIView):
    def get(self, request):
        data = dict()
        for category in RestaurantCategory.FOOD_CATEGORYS:
            data[category[1]] = category[0]
        return Response(data)

class CategoryCount(APIView):
    def get_object(self):
        if 'latitude' and 'longitude' in self.request.QUERY_PARAMS:
            latitude = self.request.QUERY_PARAMS.get('latitude', None)
            longitude = self.request.QUERY_PARAMS.get('longitude', None)
            return longlat2restaurant_set(latitude, longitude)
        else:
            raise Http404
        
    def get(self, request):
        restaurant_list = self.get_object()
        data = dict()
        for category in RestaurantCategory.FOOD_CATEGORYS:
            data[category[1]] = restaurant_list.filter(category__category=category[0]).count()
        return Response(data)

###########################################################

class RatingList(generics.ListAPIView):
    model = Rating
    serializer_class = RatingSerializer
    def get_queryset(self):
        restaurant = self.kwargs['restaurant']
        return Rating.objects.filter(restaurant=restaurant)

###########################################################

class RestaurantList(generics.ListCreateAPIView):
    model = Restaurant
    serializer_class = RestaurantSerializer
    def get_queryset(self):
        if 'latitude' and 'longitude' in self.request.QUERY_PARAMS:
            #Example: http://10.6.57.229:8000/restaurant/?latitude=40.0996345&longitude=-83.1137889
            self.serializer_class = RestaurantDistanceSerializer
            latitude = self.request.QUERY_PARAMS.get('latitude', None)
            longitude = self.request.QUERY_PARAMS.get('longitude', None)
            queryset = longlat2restaurant_set(latitude=latitude, longitude=longitude)
            
            if 'category' in self.request.QUERY_PARAMS:
                category = self.request.QUERY_PARAMS.get('category', None)
                #correct spelling if asian instead of Asian
                if category[0].islower():
                    category = category[0].capitalize() + category[1:]
                #convert tupel Asian to AS for filtering
                if category in [value for (key, value) in RestaurantCategory.FOOD_CATEGORYS]:
                    cat_index = [value for (key, value) in RestaurantCategory.FOOD_CATEGORYS].index(category)
                    category = RestaurantCategory.FOOD_CATEGORYS[cat_index][0]
                #filter or raise 404 if non existent
                if category in [key for (key, value) in RestaurantCategory.FOOD_CATEGORYS]:
                    queryset = queryset.filter(category__category=category)
                else:
                    raise Http404
            
            #default
            queryset = queryset.order_by('distance')
            
            if 'sort' in self.request.QUERY_PARAMS:
                sort = self.request.QUERY_PARAMS.get('sort', None)
                
                if sort == 'distance':
                    queryset = queryset.order_by('distance')
                if sort == 'rating':
                    #Order by rating
                    queryset = queryset.annotate(rating_avg=Avg('rating__rating')).order_by('-rating_avg')
            
            return queryset
        else:
            return Restaurant.objects.all() #change to: raise Http404

class RestaurantDetail(generics.RetrieveUpdateDestroyAPIView):
    model = Restaurant
    serializer_class = RestaurantSerializer
    
###########################################################
    
class OpeningHoursDetail(generics.RetrieveAPIView):
    model = Restaurant
    serializer_class = RestaurantOpeningHoursSerializer
    
    
class RestaurantMenuDetail(generics.RetrieveAPIView):
    model = Restaurant
    serializer_class = RestaurantMenuSerializer
    
###########################################################

class MenuSectionDetail(generics.RetrieveAPIView):
    model= MenuSection
    serializer_class= MenuSectionSerializer
    
    def get_queryset(self):
        if 'type' in self.kwargs:
            foodType = self.kwargs['type']
            mySection = MenuSection.objects.get(pk=self.kwargs['pk'])
            myItem = mySection.menu_item.get(name='Pizza')
            return MenuSection.objects.filter(menu_item=2)
        else:
            return MenuSection.objects.all()

###########################################################

class MenuItemDetail(generics.RetrieveAPIView):
    model = MenuItem
    serializer_class = MenuItemSerializer

"""
###########################################################
######## Dashboard views ##################################
###########################################################
###########################################################
"""
    
@login_required(login_url='/login/')    
def show_dashboard(request):
    username = request.user.username
    n_of_ongoing_orders = 0
    
    restaurant = get_restaurant_from_ownerId(request.user.id)    
    if (restaurant):
        n_of_ongoing_orders = count_ongoing_orders(restaurant.id)
        
    return render(request,'dash.html',{'username': username, 'n_ongoing_orders': n_of_ongoing_orders})        

@login_required(login_url='/login/')  
def show_restaurantInfo(request):
    username = request.user.username
    n_of_ongoing_orders = 0
    
    restaurant = get_restaurant_from_ownerId(request.user.id)
    if (restaurant):
        n_of_ongoing_orders = count_ongoing_orders(restaurant.id)    
    return render(request,'restaurant_info.html',{'username': username, 'restaurant':restaurant, 'n_ongoing_orders': n_of_ongoing_orders})      

@login_required(login_url='/login/') 
def show_menuSections(request):
    username = request.user.username
    menu_sections = []
    n_of_ongoing_orders = 0
    
    restaurant = get_restaurant_from_ownerId(request.user.id)    
    if (restaurant):
        n_of_ongoing_orders = count_ongoing_orders(restaurant.id)   
        menu_sections = MenuSection.objects.filter(restaurant_id=restaurant.id)
    return render(request,'menu_sections.html',{'username': username, 'menu_sections':menu_sections, 'n_ongoing_orders': n_of_ongoing_orders})      
        
            
@login_required(login_url='/login/') 
def show_menuItems(request):
    username = request.user.username
    menu_Items = {}
    n_of_ongoing_orders = 0

    restaurant = get_restaurant_from_ownerId(request.user.id)
    if (restaurant):
        n_of_ongoing_orders = count_ongoing_orders(restaurant.id) 
        menu_sections = MenuSection.objects.filter(restaurant_id=restaurant.id)
        if menu_sections:
            for menu_section in menu_sections:
                print >>sys.stderr, menu_section.id
                menu_Items[menu_section] = MenuItem.objects.filter(menu_category_id=menu_section.id)
    return render(request,'menu_items.html',{'username': username, 'menu_items':menu_Items,  'n_ongoing_orders': n_of_ongoing_orders})

def get_restaurant_from_ownerId(owner_id):
    try:
        restaurant = Restaurant.objects.filter(owner_id=owner_id)[0]
    except IndexError:
        restaurant = None  
    return restaurant  
