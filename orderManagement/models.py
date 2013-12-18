from django.db import models
from django.contrib.auth.models import User
from restaurantManagement.models import MenuItem
from userManagement.models import Address
from restaurantManagement.models import Restaurant
from django.core.exceptions import ValidationError
from django.db.models import Avg, Sum

class Order(models.Model):
    CREATING    = 0
    WAITING     = 1
    ACCEPTED    = 2
    DECLINED    = 3
    DELIVERED   = 4

    ORDER_STATUS = (
    (CREATING,      'Creating'),
    (WAITING,       'Waiting'),
    (ACCEPTED,      'Accepted'),
    (DECLINED,      'Declined'),
    (DELIVERED,     'Delivered'),
    )
    
    user = models.ForeignKey(User, related_name='order', blank=True, null= True)
    restaurant = models.ForeignKey(Restaurant, related_name='order')
    
    created = models.DateTimeField(auto_now_add=True)
    
    ##IP Address here for validation of anon users
    
    comment = models.TextField(blank=True, null= True)
    
    address = models.ForeignKey(Address, related_name='order', blank=True, null= True)
    status  = models.IntegerField(choices=ORDER_STATUS, default = 0)
    
    #implement this
    trustworthy_factor = models.IntegerField(blank=True, null= True, editable= False)
    
    def __unicode__(self):
        return 'Order: ' + str(self.id) + ' (' + self.get_status_display()+')'
    
    @property
    def total(self):
        return self.order_item.aggregate(Sum('menu_item__price'))['menu_item__price__sum']
    
    def save(self, *args, **kwargs):
        successfully_ordered = Order.objects.filter(address = self.address).filter(status = Order.DELIVERED)
        self.trustworthy_factor = len(successfully_ordered)
        return super(Order, self).save(*args, **kwargs)

    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='order_item')
    menu_item = models.ForeignKey(MenuItem, related_name='order_item')
    
    def __unicode__(self):
        return 'Order (' + str(self.order_id)+ ') - item: ' + str(self.menu_item)
    
    def clean(self):
        # Don't allow draft entries to have a pub_date.
        if self.menu_item.menu_category.restaurant != self.order.restaurant:
            raise ValidationError('You can only order items from the selected restaurant.')