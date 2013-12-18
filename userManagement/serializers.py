from django.forms import widgets
from rest_framework import serializers
from django.contrib.auth.models import User

from datetime import datetime


class PasswordField(serializers.CharField):
    
    def from_native(self, value):
        return value
        
    def to_native(self, value):
        return '*********'

class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = User
        fields = ('url','username', 'password','first_name', 'last_name' , 'email')
    
    email = serializers.EmailField(required=True)
    password = PasswordField()
    
    def save(self):
        self.object.set_password(self.object.password)
        self.object.save()
        return self.object