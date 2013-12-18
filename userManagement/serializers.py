from django.forms import widgets
from rest_framework import serializers
from django.contrib.auth.models import User
from userManagement.models import Address

from datetime import datetime

from rest_framework.reverse import reverse


class PasswordField(serializers.CharField):
    def from_native(self, value):
        return value
        
    def to_native(self, value):
        return '*********'


class UserURLSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.SerializerMethodField('get_id_url')
    class Meta:
        model = User
        fields = ('url',)
    def get_id_url(self, obj):
         return reverse('user-detail', args=[self.context['request'].user.id], request= self.context['request'])
    
    
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url','username', 'password','first_name', 'last_name' , 'email')
    
    email = serializers.EmailField(required=True)
    password = PasswordField()
    
    def save_object(self, obj, **kwargs):
        obj.set_password(obj.password)
        obj.save(**kwargs)
    
class AddressSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.HyperlinkedRelatedField(read_only=True, view_name='user-detail')
    class Meta:
        model = Address
            
class UserAddressSerializer(serializers.ModelSerializer):
    address = AddressSerializer(many = True)
    class Meta:
        model = User
        fields=('address',)