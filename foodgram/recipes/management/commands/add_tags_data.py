import csv
from django.core.management.base import BaseCommand
from recipes.models import Tag


class Command(BaseCommand):
    help = 'Load tags data to DB'

    def handle(self, *args, **options):
        with open('recipes/data/tags.csv', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                name, slug, color = row
                Tag.objects.get_or_create(name=name, slug=slug, color=color)
