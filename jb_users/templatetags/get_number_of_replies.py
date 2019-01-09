from django import template
from comments.models import Comment
from jb_users.models import User
from django.utils import timezone
register = template.Library()

@register.filter
def get_number_of_replies(username):
    user = User.objects.get(username=username)
    comments = Comment.objects.filter(user=user)
    num=0
    for comment in comments:
        if comment.parent:
            num=num+1
    return num