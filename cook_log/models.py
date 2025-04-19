from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission


# Create your models here.

class Recipe(models.Model):
    CATEGORY_CHOICES =[
        ('Dessert', 'Dessert'),
        ('Breakfast', 'Breakfast'),
        ('Main', 'Main')
    ]
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    ingredients = models.TextField(help_text="Enter ingredient separated by commas")
    instructions = models.TextField()
    category = models.CharField(max_length=255, choices=CATEGORY_CHOICES)
    preparation_time = models.PositiveIntegerField(help_text="Time in minutes")
    cooking_time = models.PositiveIntegerField(help_text="Time in minutes")
    servings = models.PositiveIntegerField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)

    groups = models.ManyToManyField(Group, related_name='customuser_set', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='customuser_permissions_set', blank=True)

    def __str__(self):
        return self.username
    

