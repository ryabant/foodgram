from django import template
from django.contrib.auth import get_user_model
from recipes.models import Follow, Favorite, ShoppingList

User = get_user_model()

register = template.Library()


@register.filter
def addclass(field, css):
    return field.as_widget(attrs={'class': css})


@register.filter(name='is_follow')
def is_follow(author, user):
    return Follow.objects.filter(user=user, author=author).exists()


@register.filter(name='is_favorite')
def is_favorite(recipe, user):
    return Favorite.objects.select_related('recipe').filter(
        user=user, recipe=recipe).exists()


@register.filter(name='is_purchased')
def is_purchased(recipe, user):
    return ShoppingList.objects.filter(user=user, recipe=recipe).exists()


@register.filter
def get_filter_values(value):
    return value.getlist('filters')


@register.filter
def get_filter_link(request, tag):
    new_request = request.GET.copy()

    if tag.slug in request.GET.getlist('filters'):
        filters = new_request.getlist('filters')
        filters.remove(tag.slug)
        new_request.setlist('filters', filters)
    else:
        new_request.appendlist('filters', tag.slug)

    return new_request.urlencode()
