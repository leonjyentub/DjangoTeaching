from django.contrib import admin

from .models import Message


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("id", "author", "short_content", "created_at", "updated_at")
    search_fields = ("content", "author__username")
    empty_value_display = "訪客"

    @admin.display(description="內容")
    def short_content(self, obj):
        return obj.content[:30]
