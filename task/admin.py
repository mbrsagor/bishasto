from django.contrib import admin
from task.models.category import Category, Post
from task.models.task import Task, TaskManager


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'parent', 'order']
    search_fields = ['name']
    list_editable = ['parent', 'order']
    list_filter = ['name', 'parent']
    list_display_links = ['name']
    list_per_page = 8


admin.site.register(Category, CategoryAdmin)


class TaskAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'status', 'task_category']
    list_filter = ['name', 'status']
    list_editable = ['status', 'task_category']
    search_fields = ['name', 'status']
    list_display_links = ['name']
    list_per_page = 8


admin.site.register(Task, TaskAdmin)


class TaskManagerAdmin(admin.ModelAdmin):
    list_display = ['id', 'tasks', 'manage_by', 'task_status', 'start_time', 'end_time', 'is_active']
    list_filter = ['tasks', 'manage_by']
    list_editable = ['task_status', 'manage_by', 'is_active']
    search_fields = ['name', 'status']
    list_display_links = ['tasks']
    list_per_page = 8


admin.site.register(TaskManager, TaskManagerAdmin)


class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'post_category']
    list_filter = ['title', 'post_category']
    search_fields = ['title', 'post_category']
    list_display_links = ['title']
    list_per_page = 8


admin.site.register(Post)
