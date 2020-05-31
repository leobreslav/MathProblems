from django.contrib import admin

# Register your models here.
from Problems.models import Task

admin.site.register(Task)