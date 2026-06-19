from django.contrib import admin
from django.http import HttpResponse

from .models import ContactMessage, Task

admin.site.site_header = "TechStore Administration"
admin.site.site_title = "TechStore Admin"
admin.site.index_title = "Welcome to TechStore Admin"


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ["title", "completed", "created_at", "updated_at"]
    list_filter = ["completed"]
    search_fields = ["title", "description"]
    date_hierarchy = "created_at"
    list_editable = ["completed"]
    list_per_page = 25
    save_on_top = True
    actions_on_bottom = True
    actions_selection_counter = True
    ordering = ["-created_at"]
    fieldsets = [
        (None, {"fields": ["title", "description"]}),
        ("Status", {"fields": ["completed"]}),
        ("Timestamps", {"fields": ["created_at", "updated_at"], "classes": ["collapse"]}),
    ]
    readonly_fields = ["created_at", "updated_at"]
    actions = ["mark_completed", "mark_pending", "export_csv"]

    @admin.action(description="Mark selected as completed")
    def mark_completed(self, request, queryset):
        updated = queryset.update(completed=True)
        self.message_user(request, f"{updated} task(s) marked as completed.")

    @admin.action(description="Mark selected as pending")
    def mark_pending(self, request, queryset):
        updated = queryset.update(completed=False)
        self.message_user(request, f"{updated} task(s) marked as pending.")

    @admin.action(description="Export selected as CSV")
    def export_csv(self, request, queryset):
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = "attachment; filename=tasks.csv"
        for task in queryset:
            response.write(f"{task.pk},{task.title},{task.completed},{task.created_at}\n")
        return response


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ["name", "email", "created_at"]
    search_fields = ["name", "email", "message"]
    date_hierarchy = "created_at"
    readonly_fields = ["name", "email", "message", "created_at"]
    actions = ["delete_old"]

    @admin.action(description="Delete messages older than 30 days")
    def delete_old(self, request, queryset):
        from datetime import timedelta
        from django.utils import timezone
        cutoff = timezone.now() - timedelta(days=30)
        old = queryset.filter(created_at__lt=cutoff)
        count = old.count()
        old.delete()
        self.message_user(request, f"{count} old message(s) deleted.")
