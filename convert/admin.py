from django.contrib import admin

from .models import ConvertTask


@admin.register(ConvertTask)
class ConvertTaskAdmin(admin.ModelAdmin):
    list_display = ["id", "state", "notion_export", "created_at", "updated_at"]
    list_filter = ["state"]
