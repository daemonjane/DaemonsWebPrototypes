from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.utils.html import format_html, mark_safe

from .models import Comment, ContactMessage, NewsletterSubscription, Task, TaskFile, UserProfile

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    fields = ["bio", "location", "phone", "avatar_url"]


class UserAdmin(BaseUserAdmin):
    inlines = [UserProfileInline]


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.site_header = "TechStore Administration"
admin.site.site_title = "TechStore Admin"
admin.site.index_title = "Welcome to TechStore Admin"


class TaskFileInline(admin.TabularInline):
    model = TaskFile
    extra = 0
    readonly_fields = ["uploaded_at"]
    fields = ["file", "name", "uploaded_at"]


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    inlines = [TaskFileInline]
    list_display = ["title", "completed", "file_count", "comment_count", "created_at", "updated_at"]
    list_filter = ["completed"]
    search_fields = ["title", "description"]
    date_hierarchy = "created_at"
    list_editable = ["completed"]
    list_per_page = 25
    list_max_show_all = 200
    save_on_top = True
    save_as = True
    actions_on_bottom = True
    actions_selection_counter = True
    show_full_result_count = True
    ordering = ["-created_at"]
    sortable_by = ["title", "completed", "created_at", "updated_at"]
    fieldsets = [
        (None, {"fields": ["title", "description", "description_preview"]}),
        ("Status", {"fields": ["completed"]}),
        ("Timestamps", {"fields": ["created_at", "updated_at"], "classes": ["collapse"]}),
    ]
    readonly_fields = ["created_at", "updated_at", "description_preview"]
    actions = ["mark_completed", "mark_pending", "export_csv"]
    actions_on_top = True
    actions_on_bottom = True

    @admin.display(description="Files")
    def file_count(self, obj):
        return obj.files.count()

    @admin.display(description="Comments")
    def comment_count(self, obj):
        return obj.comments.count()

    @admin.display(description="Preview")
    def description_preview(self, obj):
        if obj.description:
            return format_html(
                '<div class="field-description_preview">{}</div>', obj.description
            )
        return mark_safe('<span class="text-slate-600">—</span>')

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


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ["author", "task_link", "created_at", "body_preview"]
    list_filter = ["created_at", "task"]
    search_fields = ["author", "body", "task__title"]
    date_hierarchy = "created_at"
    list_per_page = 25
    list_select_related = ["task"]
    list_max_show_all = 200
    readonly_fields = ["created_at", "updated_at", "body_preview"]
    fieldsets = [
        (None, {"fields": ["task", "author", "body", "body_preview"]}),
        ("Timestamps", {"fields": ["created_at", "updated_at"], "classes": ["collapse"]}),
    ]

    @admin.display(description="body")
    def body_preview(self, obj):
        return format_html(
            '<div class="field-description_preview">{}</div>',
            obj.body[:120] + "..." if len(obj.body) > 120 else obj.body,
        )

    def task_link(self, obj):
        return format_html('<a href="{}">{}</a>', obj.task.get_absolute_url(), obj.task.title)
    task_link.short_description = "task"

    @admin.action(description="Delete selected comments")
    def delete_selected_comments(self, request, queryset):
        count = queryset.count()
        queryset.delete()
        self.message_user(request, f"{count} comment(s) deleted.")


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ["name", "email", "created_at"]
    search_fields = ["name", "email", "message"]
    date_hierarchy = "created_at"
    readonly_fields = ["name", "email", "message", "created_at", "message_preview"]
    fieldsets = [
        (None, {"fields": ["name", "email", "message", "message_preview"]}),
        ("Timestamps", {"fields": ["created_at"], "classes": ["collapse"]}),
    ]
    actions = ["delete_old"]

    @admin.display(description="Preview")
    def message_preview(self, obj):
        return format_html(
            '<div class="field-description_preview">{}</div>',
            obj.message[:200] + "..." if len(obj.message) > 200 else obj.message,
        )

    @admin.action(description="Delete messages older than 30 days")
    def delete_old(self, request, queryset):
        from datetime import timedelta
        from django.utils import timezone
        cutoff = timezone.now() - timedelta(days=30)
        old = queryset.filter(created_at__lt=cutoff)
        count = old.count()
        old.delete()
        self.message_user(request, f"{count} old message(s) deleted.")


@admin.register(NewsletterSubscription)
class NewsletterSubscriptionAdmin(admin.ModelAdmin):
    list_display = ["email", "active", "created_at"]
    list_filter = ["active"]
    search_fields = ["email"]
    date_hierarchy = "created_at"
    list_per_page = 50
    list_editable = ["active"]
    actions = ["mark_active", "mark_inactive"]

    @admin.action(description="Mark selected as active")
    def mark_active(self, request, queryset):
        updated = queryset.update(active=True)
        self.message_user(request, f"{updated} subscription(s) marked as active.")

    @admin.action(description="Mark selected as inactive")
    def mark_inactive(self, request, queryset):
        updated = queryset.update(active=False)
        self.message_user(request, f"{updated} subscription(s) marked as inactive.")


@admin.register(TaskFile)
class TaskFileAdmin(admin.ModelAdmin):
    list_display = ["filename", "task_link", "uploaded_at"]
    search_fields = ["name", "task__title"]
    date_hierarchy = "uploaded_at"
    list_select_related = ["task"]
    readonly_fields = ["uploaded_at"]

    def task_link(self, obj):
        return format_html('<a href="{}">{}</a>', obj.task.get_absolute_url(), obj.task.title)
    task_link.short_description = "task"

    def filename(self, obj):
        return obj.filename()
    filename.short_description = "file"


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "location", "phone", "created_at"]
    search_fields = ["user__username", "user__email", "location", "phone"]
    list_filter = ["location"]
    date_hierarchy = "created_at"
    readonly_fields = ["created_at", "updated_at"]
    fieldsets = [
        (None, {"fields": ["user"]}),
        ("Profile Info", {"fields": ["bio", "location", "phone", "avatar_url"]}),
        ("Timestamps", {"fields": ["created_at", "updated_at"], "classes": ["collapse"]}),
    ]
