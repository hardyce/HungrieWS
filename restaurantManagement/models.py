from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from GPS.circle import get_geolocation, within_radius 

"""
TO-DO:
restrict delivery radius
"""
from django.db import models


class Restaurant(models.Model):
    owner = models.ForeignKey(User, related_name='restaurant')
  
    name = models.CharField(max_length=100)
    street1 = models.CharField(max_length=200)
    street2 = models.CharField(max_length=200, blank=True, null= True)
    postcode = models.CharField(max_length=50)
    city =models.CharField(max_length=100)
    country =models.CharField(max_length=100)
    
    latitude = models.FloatField(editable=False, blank=True, null= True)
    longitude = models.FloatField(editable=False, blank=True, null= True)
    #delivery_range = models.DecimalField(max_digits=3, decimal_places=1, default=1)
    #This should be changed to phone field
    phone = models.CharField(max_length=50, unique = True)
    email = models.EmailField()

    preparation_time = models.TimeField(blank=True, null= True)
    delivery_minimum = models.DecimalField(max_digits=5, decimal_places=2)
    delivery_cost    = models.DecimalField(max_digits=5, decimal_places=2)
    
    def __unicode__(self):
        return self.name + ' (' + self.city + ', '+self.postcode+')'
    
    def save(self, *args, **kwargs):
        if not self.latitude and not self.longitude:
            geocode = get_geolocation(self.street1, self.postcode, self.city)
            self.latitude = geocode.get('latitude')
            self.longitude = geocode.get('longitude')

        return super(Restaurant, self).save(*args, **kwargs)
    
    def distance(self, longitude, latitude):
        return within_radius(self, {'latitude': self.latitude, 'longitude':self.longitude}, {'latitude': latitude, 'longitude':longitude})
        


class RestaurantCategory(models.Model):
    AMERICAN = 'AM'
    ASIAN = 'AS'
    CHINESE='CH'
    INDIAN='IN'
    INTERNATIONAL='INT'
    IRISH='IR'
    ITALIAN='ITA'
    JAPANESE='JAP'
    PIZZA='PIZ'
    THAI='TH'
    OTHER='OTH'
    
    FOOD_CATEGORYS= (
                    (AMERICAN, 'American'),
                    (ASIAN, 'Asian'),
                    (CHINESE, 'Chinese'),
                    (INDIAN, 'Indian'),
                    (INTERNATIONAL, 'International'),
                    (IRISH, 'Irish'),
                    (ITALIAN, 'Italian'), 
                    (JAPANESE, 'Japanese'), 
                    (PIZZA, 'Pizza'), 
                    (THAI, 'Thai'),
                    (OTHER, 'Other'),                 
    )
    category = models.CharField(max_length=3, choices=FOOD_CATEGORYS)
    restaurant = models.ForeignKey(Restaurant, related_name='category')
  
    
    def __unicode__(self):
        return self.get_category_display()


class OpeningHours(models.Model):
    MONDAY=0
    TUESDAY=1
    WEDNESDAY=2
    THURSDAY=3
    FRIDAY=4
    SATURDAY=5
    SUNDAY=6
    
    
    DAYS_OF_WEEK = (
    (MONDAY, 'Monday'),
    (TUESDAY, 'Tuesday'),
    (WEDNESDAY, 'Wednesday'),
    (THURSDAY, 'Thursday'),
    (FRIDAY, 'Friday'),
    (SATURDAY, 'Saturday'),
    (SUNDAY, 'Sunday'),
    )
    restaurant = models.ForeignKey(Restaurant, related_name='opening_hours')
    day_of_week = models.IntegerField(choices=DAYS_OF_WEEK)
    time_open = models.TimeField()
    time_close =  models.TimeField()
    
    def __unicode__(self):
        return self.get_day_of_week_display() +' '+ self.time_open.strftime("%R")  + ' - ' + self.time_close.strftime("%R") 

#########################################################################
#########################################################################
#########################################################################
#########################################################################

class MenuSection(models.Model):
    ###Like Drinks, Burger, Pizza, Hot Food
    restaurant = models.ForeignKey(Restaurant, related_name='menu_section')
    title = models.CharField(max_length=100)
    
    def __unicode__(self):
        return self.title
    

class MenuItem(models.Model):
    menu_category = models.ForeignKey(MenuSection, related_name='menu_item')
    price       = models.DecimalField(max_digits=6, decimal_places=2)
    name        = models.CharField(max_length=100)
    description = models.TextField()
    
    def __unicode__(self):
        return self.name