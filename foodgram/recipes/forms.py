from django.forms import ModelForm, CheckboxSelectMultiple
from .models import Recipe


class RecipeForm(ModelForm):
    class Meta:
        model = Recipe
        fields = ('title', 'image', 'tags', 'cooking_time', 'description')
        widgets = {'tags': CheckboxSelectMultiple()}
