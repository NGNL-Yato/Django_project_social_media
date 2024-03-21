from django import template
from backend.models import Like

register = template.Library()

@register.simple_tag
def has_liked(user, post):
    return Like.objects.filter(user=user, post=post).exists()