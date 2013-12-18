from django.db import models
from userManagement import signals
from django.contrib.auth.models import User
# Create your models here.

class Address(models.Model):
    user        = models.ForeignKey(User, related_name='address', null = True, blank=True)
    street1     = models.CharField(max_length=200)
    street2     = models.CharField(max_length=200, blank=True, null= True)
    postcode    = models.CharField(max_length=50)
    city        = models.CharField(max_length=100)
    
    #This should be changed to phone field
    phone = models.CharField(max_length=50)
    
    def __unicode__(self):
        return str(self.user) + ': ' + self.street1 + ' / ' +  self.street2 + ' / ' + self.city