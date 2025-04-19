from rest_framework import serializers
from .models import Recipe, CustomUser
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token


User = get_user_model()

class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ['title', 'description', 'ingredients', 'instructions' , 'category', 'preparation_time', 'cooking_time', 'servings', 'created_date']


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email']


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        Token.objects.create(user=user)
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(write_only=True)
