from django.contrib import admin

from .models import utilisateur, follow , Professor , Etudiant ,Enterprise , Event , Post , Like , Experience

admin.site.register(utilisateur)
admin.site.register(follow)
admin.site.register(Etudiant)
admin.site.register(Professor)
admin.site.register(Enterprise)
admin.site.register(Experience)
admin.site.register(Event)
admin.site.register(Post)
admin.site.register(Like)