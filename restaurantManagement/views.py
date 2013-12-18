from rest_framework import serializers
from restaurantManagement.serializers import RestaurantSerializer, RestaurantCategorySerializer, OpeningHoursSerializer, RestaurantOpeningHoursSerializer, RestaurantMenuSerializer, MenuItemSerializer, MenuSectionSerializer
from restaurantManagement.models import Restaurant, RestaurantCategory, MenuSection, MenuItem, OpeningHours
from rest_framework import generics
from rest_framework import authentication
from rest_framework import permissions

import django_filters
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.log import logger
import sys

"""
class RestaurantFilter(django_filters.FilterSet):
    #latitude = django_filters.NumberFilter(lookup_type='lt')
   
    class Meta:
        model = Restaurant
        fields = ['latitude']
"""


class RestaurantList(generics.ListCreateAPIView):
    model = Restaurant
    serializer_class = RestaurantSerializer
    #filter_class = RestaurantFilter
    
    #filter_fields = ('latitude','longitude',)
    
    
    #Example
    #http://10.6.57.229:8000/restaurant/?latitude=40.0996345&longitude=-83.1137889
    
    def get_queryset(self):
        if 'latitude' and 'longitude' in self.request.QUERY_PARAMS:
            
            latitude = self.request.QUERY_PARAMS.get('latitude', None)
            longitude = self.request.QUERY_PARAMS.get('longitude', None)
            
            return Restaurant.objects.filter(latitude=latitude).filter(longitude=longitude)
        else:
            return Restaurant.objects.all()

    
class RestaurantDetail(generics.RetrieveUpdateDestroyAPIView):
    model = Restaurant
    serializer_class = RestaurantSerializer
    
###########################################################
    
class RestaurantCategoryList(generics.ListCreateAPIView):
    model = RestaurantCategory
    serializer_class = RestaurantCategorySerializer
    
class RestaurantCategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    model = RestaurantCategory
    serializer_class = RestaurantCategorySerializer
    
###########################################################
    
class OpeningHoursDetail(generics.RetrieveAPIView):
    model = Restaurant
    serializer_class = RestaurantOpeningHoursSerializer#Opening_HoursSerializer
    
class RestaurantMenuDetail(generics.RetrieveAPIView):
    model = Restaurant
    serializer_class = RestaurantMenuSerializer#Opening_HoursSerializer
    
"""    
class Opening_HoursList(generics.ListCreateAPIView):
    model = Opening_Hours
    serializer_class = Opening_HoursSerializer
    
    def get_queryset(self):
        restaurant= self.kwargs['restaurant']
        return Opening_Hours.objects.filter(restaurant=restaurant)

class Opening_HoursDetail(generics.RetrieveUpdateDestroyAPIView):
    model= Opening_Hours
    serializer_class=Opening_HoursSerializer

    #def get_queryset(self):
    #    restaurant= self.kwargs['restaurant']
    #    return Opening_Hours.objects.filter(restaurant=restaurant)
"""
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


######## Dashboard views ##################################
    
@login_required(login_url='/login/')    
def show_dashboard(request):
    username = request.user.username
    return render(request,'dash.html',{'username': username})        

@login_required(login_url='/login/')  
def show_restaurantInfo(request):
    username = request.user.username
    restaurant = Restaurant.objects.get(owner_id=request.user.id)
    return render(request,'restaurant_info.html',{'username': username, 'restaurant':restaurant})      

@login_required(login_url='/login/') 
def show_menuSections(request):
    username = request.user.username
    menu_sections = []
    restaurant = Restaurant.objects.get(owner_id=request.user.id)
    if (restaurant):
        menu_sections = MenuSection.objects.filter(restaurant_id=restaurant.id)
    return render(request,'menu_sections.html',{'username': username, 'menu_sections':menu_sections})      
        
@login_required(login_url='/login/') 
def show_menuItems(request):
    username = request.user.username
    menu_Items = {}
    restaurant = Restaurant.objects.get(owner_id=request.user.id)
    if (restaurant):
        menu_sections = MenuSection.objects.filter(restaurant_id=restaurant.id)
        if menu_sections:
            for menu_section in menu_sections:
                print >>sys.stderr, menu_section.id
                menu_Items[menu_section.title] = MenuItem.objects.filter(menu_category_id=menu_section.id)
    return render(request,'menu_items.html',{'username': username, 'menu_items':menu_Items})  