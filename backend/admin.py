from django.contrib import admin

from .models import utilisateur, follow

admin.site.register(utilisateur)
admin.site.register(follow)