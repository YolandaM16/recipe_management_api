from django.shortcuts import render, get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import get_user_model
#from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer
from django.contrib.auth import authenticate
from .serializers import RegisterSerializer, LoginSerializer
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, RetrieveUpdateAPIView, UpdateAPIView
from .models import Recipe, CustomUser
from .serializers import RecipeSerializer, CustomUserSerializer

User = get_user_model()


# Create your views here.

class RecipeList(ListCreateAPIView):
    def get_queryset(self):
        return Recipe.objects.all()
    
    def get_serializer_class(self):
        return RecipeSerializer
    
class RecipeDetail(RetrieveUpdateDestroyAPIView):
    def get_queryset(self):
        return Recipe.objects.all()
    
    def get_serializer_class(self):
        return RecipeSerializer

class CustomUserList(ListCreateAPIView):
    def get_queryset(self):
        return CustomUser.objects.all()
    
    def get_serializer_class(self):
        return CustomUserSerializer
    
class CustomUserDetail(RetrieveUpdateDestroyAPIView):
    def get_queryset(self):
        return CustomUser.objects.all()
    
    def get_serializer_class(self):
        return CustomUserSerializer
    
class RegisterView(generics.CreateAPIView):
    def get_queryset(self):
        return User.objects.all()
    
    def get_serializer_class(self):
        return RegisterSerializer
    
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)

        user = User.objects.get(username=response.data.get('username'))
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, 'user': response.data})


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(username=serializer.validated_data['username'], password=serializer.validated_data['password'])
        
        
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key, 'user': {"username": user.username, "email": user.email}})
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        

class UserProfileView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    def get_object(self):
        return self.request.user