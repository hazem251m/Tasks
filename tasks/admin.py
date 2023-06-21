from django.contrib import admin
from .models import Task,TaskNotes
# Register your models here.


admin.site.register(Task)
admin.site.register(TaskNotes)