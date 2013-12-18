from django.contrib.auth.models import User
from userManagement.serializers import UserSerializer
from rest_framework import generics
from rest_framework import authentication
from rest_framework import permissions

from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.template.context import RequestContext
import restaurantManagement
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse


class UserList(generics.ListCreateAPIView):
    model = User
    serializer_class = UserSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    #permission_classes = (permissions.IsAuthenticated,)
    

    #This view should return a list of all the details
    #for the currently authenticated user.
    
    def get_queryset(self):
        user = self.request.user.id
        return self.model.objects.filter(id=user)


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    model = User
    serializer_class = UserSerializer

    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user.id
        return self.model.objects.filter(id=user)

######## login & logout views used to access the restaurant's dashboard #####   
def login_user(request):
    state = ""
    username = password = ''
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                state = "You're successfully logged in!"
                ##return HttpResponseRedirect(reverse(restaurantManagement.views.show_dashboard, args=[request]))
                return HttpResponseRedirect("/dashboard")
            else:
                state = "Your account is not active, please contact the site admin."
        else:
            state = "Your username and/or password were incorrect."
    ##return render_to_response("auth.html", {'state':state, 'username': username}, context_instance = RequestContext(request))
    return render(request,'auth.html',{'state':state, 'username': username})

def logout_user(request):
    state = "Successful logged out"
    logout(request)
    return render(request,'auth.html',{'state':state})   
