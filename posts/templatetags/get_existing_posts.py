from django import template
from posts.models import Post
from django.utils import timezone
register = template.Library()

@register.simple_tag
def get_existing_posts(): 
    existing_posts = Post.objects.all().order_by("-timestamp")[:7]
    # print(existing_posts)
    # print("list of six posts:",existing_posts[:3],existing_posts[3:5],existing_posts[5:])
    posts ={
        existing_posts[:2],
        existing_posts[3:5],
        existing_posts[5:7],
        }
    # print(posts)
    return posts