from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Ingredient(models.Model):
    title = models.CharField(max_length=256)
    dimension = models.CharField(max_length=256)

    def __str__(self):
        return '{title}, ({dimension})'.format(title=self.title, dimension=self.dimension)


class Tag(models.Model):
    name = models.CharField(max_length=20)
    slug = models.SlugField(max_length=20, unique=True)
    color = models.CharField(max_length=20)

    def __str__(self):
        return '{name}, ({color})'.format(name=self.name, color=self.color)


class Recipe(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='recipes')
    title = models.CharField(max_length=256)
    image = models.ImageField(upload_to='recipes/', blank=True, null=True)
    description = models.TextField(max_length=1024)
    cooking_time = models.PositiveIntegerField()
    ingredients = models.ManyToManyField(Ingredient, through='RecipeIngredient')
    tags = models.ManyToManyField(Tag)
    pub_date = models.DateTimeField('date published', auto_now_add=True)

    class Meta:
        ordering = ['-pub_date']

    def __str__(self):
        return self.title


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='recipeingredients')
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE,
                                   related_name='recipeingredients')
    amount = models.PositiveIntegerField()

    def __str__(self):
        return '{recipe} - {ingredient}, {amount}'.format(
            recipe=self.recipe, ingredient=self.ingredient, amount=self.amount)


class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="follower")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")

    def __str__(self):
        return self.user.username


class Favorite(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='favorites')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="favorites")

    def __str__(self):
        return self.recipe.title


class ShoppingList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='purchases')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='purchases')

    def __str__(self):
        return self.recipe.title
