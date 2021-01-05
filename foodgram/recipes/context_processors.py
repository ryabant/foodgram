from .models import ShoppingList


def counter(request):
    if request.user.is_authenticated:
        count = ShoppingList.objects.filter(user=request.user).count()
    else:
        count = None
    return {"shop_list_count": count}
