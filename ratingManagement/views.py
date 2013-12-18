from rest_framework import generics
from rest_framework import authentication
from rest_framework import permissions
from ratingManagement.serializers import RatingSerializer
from ratingManagement.serializers import Rating
from django.contrib.auth.models import User
from django import http

class RatingCreate(generics.CreateAPIView):
    model = Rating
    serializer_class = RatingSerializer
    permission_classes = (permissions.IsAuthenticated,)
    
class RatingDetail(generics.RetrieveAPIView):
    model = Rating
    serializer_class = RatingSerializer