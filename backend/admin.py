from django.contrib import admin

from .models import utilisateur, follow , Professor , Etudiant ,Enterprise , Event , Post , Like , Experience , Skills,Languages,Education,Certification,ClassRoom,PostClassroom,Task,TaskResponse

admin.site.register(utilisateur)
admin.site.register(follow)
admin.site.register(Etudiant)
admin.site.register(Professor)
admin.site.register(Enterprise)
admin.site.register(Experience)
admin.site.register(Event)
admin.site.register(Post)
admin.site.register(Like)
admin.site.register(Skills)
admin.site.register(Languages)
admin.site.register(Education)
admin.site.register(Certification)
admin.site.register(ClassRoom)
admin.site.register(PostClassroom)
admin.site.register(Task)
admin.site.register(TaskResponse)



