from django import template
from category.models import Category
from django.utils import timezone

register = template.Library()

@register.filter
def month_to_str(text):
    val = ""
    if text == 1:
        val = "Jan"
    elif text == 2:
        val ="Feb"
    elif text == 3:
        val = "Mar"
    elif text == 4:
        val = "Apr"
    elif text == 5:
        val ="May"
    elif text == 6:
        val = "Jun"
    elif text == 7:
        val = "Jul"
    elif text == 8:
        val ="Aug"
    elif text == 9:
        val = "Sep"
    elif text == 10:
        val = "Oct"
    elif text == 11:
        val ="Nov"
    elif text == 12:
        val = "Dec"
    return val