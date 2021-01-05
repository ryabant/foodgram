import json
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.views.decorators.http import require_http_methods
from django.shortcuts import get_object_or_404
from recipes.models import Ingredient, Recipe, Follow, Favorite, ShoppingList

User = get_user_model()


@require_http_methods(["GET"])
def get_ingredients(request):
    query = request.GET.get('query', [])
    ingredients_query = Ingredient.objects.filter(
        title__istartswith=query).values(
        'title', 'dimension')
    response = list(ingredients_query)
    return JsonResponse(response, safe=False)


@login_required
@require_http_methods(['POST', 'DELETE'])
def follow_user(request, author_id):
    if request.method == 'POST':
        author_id = json.loads(request.body).get('id')
        author = get_object_or_404(User, id=author_id)
        obj, created = Follow.objects.get_or_create(user=request.user, author=author)
        return JsonResponse({'success': created})

    elif request.method == 'DELETE':
        author = get_object_or_404(User, id=author_id)
        removed = Follow.objects.filter(user=request.user, author=author).delete()
        return JsonResponse({'success': bool(removed)})


@login_required
@require_http_methods(['POST', 'DELETE'])
def favorite_recipe(request, recipe_id):

    if request.method == 'POST':
        recipe_id = json.loads(request.body).get('id')
        recipe = get_object_or_404(Recipe, id=recipe_id)
        obj, created = Favorite.objects.get_or_create(user=request.user, recipe=recipe)
        return JsonResponse({'success': created})

    elif request.method == 'DELETE':
        recipe = get_object_or_404(Recipe, id=recipe_id)
        removed = Favorite.objects.filter(user=request.user, recipe=recipe).delete()
        return JsonResponse({'success': bool(removed)})


@login_required
@require_http_methods(['POST', 'DELETE'])
def shopping_list(request, recipe_id):

    if request.method == 'POST':
        recipe_id = json.loads(request.body).get('id')
        recipe = get_object_or_404(Recipe, id=recipe_id)
        obj, created = ShoppingList.objects.get_or_create(user=request.user, recipe=recipe)
        return JsonResponse({'success': created})

    elif request.method == 'DELETE':
        recipe = get_object_or_404(Recipe, id=recipe_id)
        removed = ShoppingList.objects.filter(user=request.user, recipe=recipe).delete()
        return JsonResponse({'success': bool(removed)})
