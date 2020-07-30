from django.db import models
import bcrypt

class User(models.Model):
    f_name = models.CharField(max_length=60)
    l_name = models.CharField(max_length=60)
    email = models.EmailField(max_length=254)
    pw_hash = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
class Meal(models.Model):
    name= models.CharField(max_length=100)
    meal_number = models.IntegerField()
    created_at= models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now=True)
    users_who_saved= models.ManyToManyField(User, related_name="saved_meals")
class Friend(models.Model):
    f_name= models.CharField(max_length=45)
    l_name= models.CharField(max_length=45)
    created_at= models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now=True)
    friended_users= models.ManyToManyField(User, related_name="friends")
class Profile(models.Model):
    age= models.IntegerField()
    location= models.CharField(max_length=45)
    desc= models.CharField(max_length=255)
    cooking_level= models.CharField(max_length=45)
    user= models.ForeignKey(User, related_name="profile", on_delete=models.CASCADE)
# Create your models here.
