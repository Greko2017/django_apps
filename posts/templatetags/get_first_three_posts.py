from django import template
from posts.models import Post
from django.utils import timezone
register = template.Library()

@register.simple_tag
def get_first_three_posts(): 
    existing_posts = Post.objects.all().order_by("-timestamp")[:3]
    posts = []
    for post in existing_posts:
        posts.append(post)    
    print("The first three posts are: ",posts)
    return posts