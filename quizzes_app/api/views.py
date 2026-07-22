from rest_framework.views import APIView
from rest_framework.permissions import  IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate

class QuizzesView(APIView):
    pass

class QuizzesDetailView(APIView):
    pass