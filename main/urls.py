from django.urls import path     
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.validate_registration),
    path('login', views.validate_login),
    path('profile/<int:id>', views.profile),
    path('search_new_meal', views.search_new_meal),
    path('logout', views.logout),
    path('search_food', views.search_meals),
    path('food_list', views.food_list),
    path('recipe_info/<int:food_id>', views.recipe_info),
    path('search_random', views.search_random),
    path('random_meal', views.random_meal),
    path('add_fav/<food_name>/<int:food_id>', views.add_fav),
    path('remove_meal/<int:food_id>', views.remove_meal)
]