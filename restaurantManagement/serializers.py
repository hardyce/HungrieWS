from rest_framework import serializers
from restaurantManagement.models import Restaurant, RestaurantCategory, MenuSection, MenuItem, OpeningHours

class RestaurantSerializer(serializers.HyperlinkedModelSerializer):
    category = serializers.ManyRelatedField()

    class Meta:
        model = Restaurant

class RestaurantCategorySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = RestaurantCategory
        fields = ('category', 'restaurant')

class OpeningHoursSerializer(serializers.ModelSerializer):
    day_of_week = serializers.SerializerMethodField('get_day')
    time_open   = serializers.SerializerMethodField('get_time_open')
    time_close  = serializers.SerializerMethodField('get_time_close')
    class Meta:
        model= OpeningHours
        fields = ('day_of_week', 'time_open','time_close')
    
    def get_day(self, obj):
        return obj.get_day_of_week_display()
    
    def get_time_open(self, obj):
        return obj.time_open.strftime("%R")
    
    def get_time_close(self, obj):
        return obj.time_close.strftime("%R")

class RestaurantOpeningHoursSerializer(serializers.ModelSerializer):
    opening_hours = OpeningHoursSerializer()
    class Meta:
        model= Restaurant
        fields = ('opening_hours',)
    
#################################################################################

class RestaurantMenuSerializer(serializers.ModelSerializer):
    menu_section = serializers.ManyHyperlinkedRelatedField(view_name='menu')
    
    class Meta:
        model= Restaurant
        fields = ('menu_section',)
        
#################################################################################

class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields=('price', 'name', 'description')
        
class MenuSectionSerializer(serializers.HyperlinkedModelSerializer):
    menu_item = MenuItemSerializer()
    
    class Meta:
        model = MenuSection
        fields=('restaurant','title','menu_item')