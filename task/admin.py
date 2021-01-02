from django.contrib import admin
from task.models.category import Category
from task.models.task import Task, TaskManager

admin.site.register(Category)
admin.site.register(Task)
admin.site.register(TaskManager)
