from django.contrib import admin
from .models import Todo, Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'user__email', )
    search_fields = ('name',)


@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'user', 'status', 'category', 'created_at')
    list_filter = ('status', 'category', 'created_at')
    search_fields = ('title', 'description', 'user__email')
    ordering = ('-created_at',)
    raw_id_fields = ('user',)  # For better performance when selecting users
