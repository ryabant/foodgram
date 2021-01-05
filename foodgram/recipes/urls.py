from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('new/', views.new_recipe, name='new_recipe'),
    path('follow/', views.follow, name='follow'),
    path('favorite/', views.favorite, name='favorite'),
    path('purchases/', views.shoppinglist, name='purchases'),
    path('<username>/', views.profile, name='profile'),
    path('<username>/<int:recipe_id>/', views.recipe_view, name='recipe'),
    path('<str:username>/<int:recipe_id>/edit', views.recipe_edit, name='recipe_edit'),
    path('<str:username>/<int:recipe_id>/delete', views.recipe_delete, name='recipe_delete'),
    path('download_card', views.shoplist, name='download_card'),
]
