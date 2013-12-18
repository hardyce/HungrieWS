from rest_framework import serializers
from restaurantManagement.models import Restaurant, RestaurantCategory, MenuSection, MenuItem, OpeningHours

###GEO Field
import json
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.geos import *

class GeometryField(serializers.WritableField):
    """
    A field to handle GeoDjango Geometry fields
    """
    type_name = 'GeometryField'
    def to_native(self, value):
        # Gets GeoDjango geojson serialization and then convert it _back_ to a Python object
        if isinstance(value, dict) or value is None:
            return value
        raw_dict =  json.loads(value.geojson)
        result_dict = dict()
        result_dict['latitude'] = (raw_dict['coordinates'])[0]
        result_dict['longitude'] = (raw_dict['coordinates'])[1]
        return result_dict
        
class RestaurantSerializer(serializers.HyperlinkedModelSerializer):
    category = serializers.ManyRelatedField()
    location = GeometryField(required=False)
    rating = serializers.Field(source='avg_rating')
    class Meta:
        model = Restaurant

class RestaurantDistanceSerializer(serializers.HyperlinkedModelSerializer):
    category = serializers.ManyRelatedField()
    distance_km = serializers.Field(source='distance.km')
    location = GeometryField(required=False)
    rating = serializers.Field(source='avg_rating')
    class Meta:
        model = Restaurant

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
class MenuSectionListSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model= MenuSection
        fields=( 'title', 'url')

class RestaurantMenuSerializer(serializers.ModelSerializer):
    menu_section = MenuSectionListSerializer()
    class Meta:
        model= Restaurant
        fields = ('menu_section',)
        
#################################################################################

class MenuItemSerializer(serializers.HyperlinkedModelSerializer):
    faved = serializers.Field(source='faved')
    class Meta:
        model = MenuItem
        fields=('url', 'price', 'name', 'description', 'faved',) #, 'menu_category' 
        
class MenuSectionSerializer(serializers.HyperlinkedModelSerializer):
    menu_item = MenuItemSerializer()
    class Meta:
        model = MenuSection
        fields=('url', 'restaurant','title','menu_item')