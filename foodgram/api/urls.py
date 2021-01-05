from django.urls import path
from . import views

urlpatterns = [
    path('ingredients/', views.get_ingredients),
    path('<int:author_id>/subscriptions/', views.follow_user),
    path('<int:recipe_id>/favorites/', views.favorite_recipe),
    path('<int:recipe_id>/purshases/', views.shopping_list),
]
