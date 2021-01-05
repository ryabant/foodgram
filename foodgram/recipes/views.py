import csv
from django.core.paginator import Paginator
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .forms import RecipeForm
from .models import Recipe, RecipeIngredient, Ingredient, Follow, Favorite, ShoppingList, Tag


User = get_user_model()


def index(request):
    recipes_list = Recipe.objects.order_by('-pub_date').all()

    filters = request.GET.getlist('filters')
    if filters:
        recipes_list = Recipe.objects.filter(tags__slug__in=filters).distinct()
    all_tags = Tag.objects.all()

    paginator = Paginator(recipes_list, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    if request.user.is_authenticated:
        return render(
            request, 'indexAuth.html',
            {'page': page, 'paginator': paginator, 'all_tags': all_tags, })
    return render(
        request, 'indexNotAuth.html',
        {'page': page, 'paginator': paginator, 'all_tags': all_tags, })


def get_ingredients(request):
    ingredients = {}
    for key, ingredient_title in request.POST.items():
        if 'nameIngredient' in key:
            _ = key.split('_')
            ingredients[ingredient_title] = int(request.POST[f'valueIngredient_{_[1]}'])
    return ingredients


@login_required
def new_recipe(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST or None, files=request.FILES or None)
        ingredients = get_ingredients(request)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()
            for title, amount in ingredients.items():
                ingredient = get_object_or_404(Ingredient, title=title)
                recipe_ing = RecipeIngredient(recipe=recipe, ingredient=ingredient, amount=amount)
                recipe_ing.save()
            form.save_m2m()
            return redirect('index')
    else:
        form = RecipeForm()
    return render(request, 'formRecipe.html', {'form': form})


@login_required
def recipe_edit(request, username, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    if request.user != recipe.author:
        return redirect('recipe', username=username, recipe_id=recipe_id)
    form = RecipeForm(request.POST or None, files=request.FILES or None, instance=recipe)
    if request.method == 'POST':
        ingredients = get_ingredients(request)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.save()
            RecipeIngredient.objects.filter(recipe=recipe).delete()
            for title, amount in ingredients.items():
                ingredient = get_object_or_404(Ingredient, title=title)
                recipe_ing = RecipeIngredient(recipe=recipe, ingredient=ingredient, amount=amount)
                recipe_ing.save()
            form.save_m2m()
            return redirect('recipe', recipe_id=recipe.id, username=request.user.username)
    return render(request, "formChangeRecipe.html", {'form': form, 'recipe': recipe})


@login_required
def recipe_delete(request, username, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    author = get_object_or_404(User, id=recipe.author_id)
    if request.user != author:
        return redirect("recipe", username=username, recipe_id=recipe_id)
    recipe.delete()
    return redirect("profile", username=username)


def recipe_view(request, username, recipe_id):
    profile = get_object_or_404(User, username=username)
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    return render(request, 'recipe.html', {'profile': profile, 'recipe': recipe})


def profile(request, username):
    profile = get_object_or_404(User, username=username)
    recipes_list = Recipe.objects.filter(
        author=profile).order_by("-pub_date").all()
    filters = request.GET.getlist('filters')
    if filters:
        recipes_list = Recipe.objects.filter(
            tags__slug__in=filters).distinct()
    all_tags = Tag.objects.all()
    number_of_recipe = recipes_list.count()
    paginator = Paginator(recipes_list, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(
        request, "profile.html",
        {'profile': profile, 'page': page, 'paginator': paginator,
         'number_of_recipe': number_of_recipe, 'all_tags': all_tags})


@login_required
def follow(request):
    follows = Follow.objects.filter(user=request.user).all()
    paginator = Paginator(follows, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, "follow.html",
                  {'page': page, 'paginator': paginator, 'follows': follows})


@login_required
def favorite(request):
    follow_recipe = Favorite.objects.filter(user=request.user).values_list("recipe_id", flat=True)
    recipe_list = Recipe.objects.filter(id__in=follow_recipe).order_by("-pub_date").all()
    paginator = Paginator(recipe_list, 6)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)
    return render(request, "favorite.html", {"page": page, "paginator": paginator})


@login_required
def shoppinglist(request):
    purchases = ShoppingList.objects.select_related('recipe').filter(
        user=request.user)
    return render(request, 'purchases.html', {"purchases": purchases})


def shoplist(request):
    recipes = Recipe.objects.filter(purchases__user=request.user)

    ingredients_needed: dict = {}

    for recipe in recipes:
        ingredients = recipe.ingredients.values_list('title', 'dimension')
        content = recipe.recipeingredients.values_list('amount', flat=True)

        for num in range(len(ingredients)):
            title: str = ingredients[num][0]
            dimension: str = ingredients[num][1]
            amount: int = content[num]

            if title in ingredients_needed.keys():
                ingredients_needed[title] = [ingredients_needed[title][0] + amount, dimension]
            else:
                ingredients_needed[title] = [amount, dimension]

    response = HttpResponse(content_type='txt/csv')
    writer = csv.writer(response)

    for key, value in ingredients_needed.items():
        writer.writerow([f'{key} ({value[1]}) - {value[0]}'])

    return response
