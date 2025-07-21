from django.contrib import admin
from .models import Todo

# Register your models here.


@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "owner", "is_completed", "created_at",)
    list_filter = ("is_completed", "owner",)
    search_fields = ("title", "description", "owner__username",)
    ordering = ("-created_at",)
    list_per_page = 20

    actions = ("mark_complete",)

    def mark_complete(self, request, queryset):
        queryset.update(is_completed=True)
