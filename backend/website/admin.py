from django.contrib import admin

from .models import ContactMessage, Task

admin.site.site_header = "TechStore Administration"
admin.site.site_title = "TechStore Admin"
admin.site.index_title = "Welcome to TechStore Admin"


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ["title", "completed", "created_at"]
    list_filter = ["completed"]
    search_fields = ["title"]


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ["name", "email", "created_at"]
