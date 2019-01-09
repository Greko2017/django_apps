from django import template
from posts.models import Post
from jb_users.models import User
from django.utils import timezone
register = template.Library()

@register.filter
def get_number_of_articles(username):
    user = User.objects.get(username=username)
    posts = Post.objects.filter(user=user)
    num=0
    for post in posts:
        num=num+1
    return num