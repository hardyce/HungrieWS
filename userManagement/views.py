from django.contrib.auth.models import User
from userManagement.serializers import UserSerializer, UserAddressSerializer, AddressSerializer, UserURLSerializer, AddressSerializer
from userManagement.models import Address
from rest_framework import generics, mixins
from rest_framework import authentication
from rest_framework import permissions
from userManagement.permissions import IsUser, IsAddressUser, IsUserURL

#### Functional API VIew
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

####Dashboard
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.template.context import RequestContext
import restaurantManagement
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

class RetrieveUserID(APIView):
    def get_object(self):
        try:
            user_id = self.request.user.id
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            raise Http404
        
    def get(self, request, format=None):
        user = self.get_object()
        serializer = UserURLSerializer(user, context={'request': request})
        return Response(serializer.data)

class UserList(generics.CreateAPIView):
    model = User
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    model = User
    serializer_class = UserSerializer
    permission_classes = (IsUser,)  
    
    def pre_save(self, obj):
        obj.set_password("partz")##obj.password)
    
class AddressList(generics.ListAPIView):
    model = Address
    serializer_class = AddressSerializer
    permission_classes = (IsUserURL,)
    
    def get_queryset(self):
        user_id = self.kwargs['user']
        return Address.objects.filter(user__id = user_id)

class AddressCreater(generics.CreateAPIView):
    model = Address
    serializer_class = AddressSerializer
    
    def pre_save(self, obj):
        if isinstance(self.request.user , User):   
            setattr(obj, 'user', self.request.user)
        else:
            setattr(obj, 'user', None)    

class AddressDetail(generics.RetrieveAPIView):
    model = Address
    serializer_class = AddressSerializer
    permission_classes = (IsAddressUser,)
    

"""
Dashboard
"""

######## login & logout views used to access the restaurant's dashboard #####   
def login_user(request):
    state = ""
    username = password = ''
    error = True
    
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                if user.groups.filter(name='owners').count():
                    login(request, user)
                    error = False
                    return HttpResponseRedirect("/dashboard")
                elif user.groups.filter(name='users').count():
                    login(request, user)
                    error = False
                    return HttpResponseRedirect("/home")
                else:
                    state = "Your account does not have permissions to access, please contact the site admin."
            else:
                state = "Your account is not active, please contact the site admin."
        else:
            state = "Your username and/or password were incorrect."
    ##return render_to_response("auth.html", {'state':state, 'username': username}, context_instance = RequestContext(request))
    return render(request,'auth.html',{'state':state, 'username': username, 'error' : error})

def logout_user(request):
    state = "Successful logged out"
    logout(request)
    return render(request,'auth.html',{'state':state})   
