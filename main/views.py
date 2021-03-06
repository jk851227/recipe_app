from django.shortcuts import render, redirect
from datetime import datetime
from django.contrib import messages
from .models import User, Meal, Profile, Friend
import bcrypt
from .forms import RegisterForm, LoginForm
import requests

def index(request):
    request.session['user'] = ""
    context = {
        'register_form' : RegisterForm(),
        'login_form' : LoginForm(),
        'all_users' : User.objects.all()
    }
    return render(request, "login.html", context)

def validate_login(request):
    this_user_email = request.POST['email']
    request.session['user'] = this_user_email
    this_user = User.objects.get(email=this_user_email)
    request.session['user_id'] = this_user.id
    if not bcrypt.checkpw(request.POST["pw_hash"].encode(), this_user.pw_hash.encode()):
        messages.error(request, "Incorrect Password")
        return redirect("/")
    return redirect(f"/profile/{this_user.id}")

def validate_registration(request):
    password = request.POST['pw_hash']
    if password != request.POST['confirm_pw']:
        messages.error(request, "Passwords must match")
        return redirect("/")
    pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode() 
    User.objects.create(
        f_name=request.POST['f_name'],
        l_name=request.POST['l_name'],
        email=request.POST['email'],
        pw_hash=pw_hash,
    )
    new_user_email = request.POST['email']
    this_user = User.objects.get(email=new_user_email)
    request.session['user'] = new_user_email
    return redirect(f"/profile/{this_user.id}")

def profile(request, id):
    this_user = User.objects.get(id=id)
    if this_user.email != request.session['user']:
        messages.error(request, "User authentication required")
        return redirect("/")
    meals = this_user.saved_meals.all()
    context = {
        'user' : this_user,
        'meals': meals
    }
    return render(request, "profile.html", context)

def profile_form(request):
    origin = User.objects.get(email=request.session['user'])
    context = {
        'user': origin
    }
    return render(request, 'profile_form.html', context)

def update_profile(request):
    origin= User.objects.get(email=request.session['user'])
    context = {
        'user': origin,
        'user_profile': origin.profile.first()
    }
    return render(request, 'update_form.html', context)

def addProfile(request):
    Profile.objects.create(
        age= request.POST['age'],
        location= request.POST['location'],
        desc= request.POST['desc'],
        cooking_level= request.POST['cooking_level'],
        user= User.objects.get(id=request.POST['user'])
    )
    user= User.objects.get(id=request.POST['user'])
    return redirect(f"/profile/{user.id}")

def addUpdate(request):
    user = User.objects.get(id=request.POST['user'])
    profile_update= user.profile.first()
    profile_update.age= request.POST['age']
    profile_update.location= request.POST['location']
    profile_update.desc= request.POST['desc']
    profile_update.cooking_level= request.POST['cooking_level']
    profile_update.save()
    return redirect(f"/profile/{user.id}")

def search_new_meal(request):
    current_user = User.objects.get(email=request.session['user'])
    context = {
        'user': current_user
    }
    return render(request, "index.html", context)

def search_meals(request):
    url = 'https://api.spoonacular.com/recipes/findByIngredients?apiKey=ba2645667f5b40a3a7d42da11db66def&ingredients={}'
    ingredients = request.POST['ingredients']
    foods = requests.get(url.format(ingredients)).json()
    request.session['foods'] = foods
    return redirect('/food_list')

def food_list(request):
    current_user = User.objects.get(email=request.session['user'])
    foods = request.session['foods']
    meals = current_user.saved_meals.all()
    context = {
        'foods': foods,
        'user': current_user,
        'meals': meals
    }
    return render(request, 'food_list.html', context)

def recipe_info(request, food_id):
    url = 'https://api.spoonacular.com/recipes/{}/information?apiKey=ba2645667f5b40a3a7d42da11db66def&includeNutrition=false'
    recipe_info = requests.get(url.format(food_id)).json()
    current_user = User.objects.get(email=request.session['user'])
    all_ingredients = recipe_info['extendedIngredients']
    instructions = recipe_info['instructions']
    if current_user.saved_meals.filter(meal_number=food_id):
        user_saved_meal = current_user.saved_meals.get(meal_number=food_id).meal_number
    else:
        user_saved_meal = None

    context = {
        'food': recipe_info,
        'all_ingredients': all_ingredients,
        'instructions': instructions,
        'user': current_user,
        'user_saved_meal': user_saved_meal,

    }
    return render(request, 'recipe_info.html', context)

def search_random(request):
    url = 'https://api.spoonacular.com/recipes/random?apiKey=ba2645667f5b40a3a7d42da11db66def&number=1'
    random_meal = requests.get(url).json()
    request.session['food'] = random_meal['recipes'][0]
    return redirect('/random_meal')

def random_meal(request):
    current_user = User.objects.get(email=request.session['user'])
    food = request.session['food']
    context = {
        'user': current_user,
        'food': food
    }
    return render(request, 'random_meal.html', context)

def add_fav(request, food_name, food_id):
    current_user = User.objects.get(email=request.session['user'])
    new_meal = Meal.objects.create(name=food_name, meal_number=food_id)
    new_meal.users_who_saved.add(current_user)
    return redirect(f'/profile/{current_user.id}')

def remove_meal(request, food_id):
    current_user = User.objects.get(email=request.session['user'])
    current_meal = Meal.objects.get(id=food_id)
    current_user.saved_meals.remove(current_meal)
    current_user.save()
    return redirect(f'/profile/{current_user.id}')

def logout(request):
    request.session.flush()
    return redirect("/")
