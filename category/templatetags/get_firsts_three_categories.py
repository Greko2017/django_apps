from django import template
from category.models import Category
from django.utils import timezone

register = template.Library()

@register.simple_tag
def get_firsts_three_categories(): 
    categories = Category.objects.get_first_three_categories()
    categories_tbl = []
    for category in categories:
        categories_tbl.append(category)
    print(categories_tbl)
    return categories_tbl