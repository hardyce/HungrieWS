from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
from restaurantManagement.models import Restaurant, MenuItem

###Validation
from django.db.models import F
from django.core.exceptions import ValidationError

#limit_choices_to = {'menu_category__restaurant': 2})

class Rating(models.Model):
    user = models.ForeignKey(User, related_name='rating')
    restaurant = models.ForeignKey(Restaurant, related_name='rating')
    rating = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])
    fav_menu_item = models.ForeignKey(MenuItem, related_name='rating', null=True, blank = True)
    comment = models.TextField(null=True, blank = True)
    
    def __unicode__(self):
        return self.restaurant.name + ": " + str(self.rating) + "/5 by " + self.user.username
    
    """
    def clean(self):
        if self.restaurant != self.fav_menu_item.menu_category.restaurant:
            raise ValidationError('Menu item must be from the same restaurant.')
        
        if self.user.order.filter(restaurant=self.restaurant).filter(status=4).count() == 0:
            raise ValidationError('Ratings are only allowed when you have previously ordered at this restaurant.')
        
        if self.user.rating.filter(restaurant=self.restaurant).count() > 0:
            raise ValidationError('You can only vote once for a restaurant.')
    """
            

