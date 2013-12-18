from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

@login_required(login_url='/login/') 
def index(request):
    username = request.user.username    
    return render(request, 'main.html', {'username': username})

def jquery(request):
    return render(request, 'jquery-1.9.1.min.js')