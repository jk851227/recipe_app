from django.db import models
import bcrypt
class UserManager(models.Manager):
    def profile_validator(self, post_data):
        errors = {}
        if len(post_data['age']) < 1:
            errors['age'] = "Age must be provided!"
        if len(post_data['location']) < 1:
            errors['location'] = "Location must be provided!"
        return errors
class User(models.Model):
    f_name = models.CharField(max_length=60)
    l_name = models.CharField(max_length=60)
    email = models.EmailField(max_length=254)
    pw_hash = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
class Meal(models.Model):
    name= models.CharField(max_length=100)
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
    objects= UserManager()
# Create your models here.
