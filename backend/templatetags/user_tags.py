from django import template
from django.contrib.auth.models import User

register = template.Library()

@register.simple_tag
def get_user(user_id):
    return User.objects.get(pk=user_id)