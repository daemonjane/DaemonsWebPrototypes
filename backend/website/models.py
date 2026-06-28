from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class UserProfile(
    """Extended user profile model with additional fields."""models.Model):
    """Extended profile information for users."""

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    bio = models.TextField("bio", blank=True, help_text="A short bio about yourself")
    location = models.CharField("location", max_length=100, blank=True, help_text="Your location")
    phone = models.CharField("phone", max_length=20, blank=True, help_text="Contact phone number")
    avatar_url = models.URLField("avatar URL", blank=True, help_text="URL to your avatar image")
    created_at = models.DateTimeField(auto_now_add=True, help_text="Timestamp when the profile was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="Timestamp when the profile was last updated")

    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"
        ordering = ["user__username"]

    def __str__(self):
        return f"Profile of {self.user.username}"


class NewsletterSubscription(models.Model):
    """An email subscriber to the TechStore newsletter."""

    email = models.EmailField("email", unique=True, help_text="Subscriber email address")
    active = models.BooleanField("active", default=True, help_text="Whether the subscription is active")
    created_at = models.DateTimeField(auto_now_add=True, help_text="Timestamp when the subscription was created")

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Newsletter Subscription"
        verbose_name_plural = "Newsletter Subscriptions"

    def __str__(self):
        return self.email


class Comment(models.Model):
    """A comment attached to a task."""

    task = models.ForeignKey("Task", on_delete=models.CASCADE, related_name="comments", help_text="The task this comment belongs to")
    author = models.CharField("author", max_length=100, help_text="Your name or display name")
    body = models.TextField("body", help_text="Your comment text")
    created_at = models.DateTimeField(auto_now_add=True, help_text="Timestamp when the comment was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="Timestamp when the comment was last updated")

    class Meta:
        ordering = ["created_at"]
        verbose_name = "Comment"
        verbose_name_plural = "Comments"

    def __str__(self):
        return f"{self.author} on {self.task.title}"


class Task(models.Model):
    """A to-do task with completion tracking."""

    title = models.CharField("title", max_length=200, help_text="A short, descriptive title for the task")
    description = models.TextField("description", blank=True, help_text="Optional longer description of what the task involves")
    completed = models.BooleanField("completed", default=False, help_text="Mark as completed when the task is finished")
    created_at = models.DateTimeField(auto_now_add=True, help_text="Timestamp when the task was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="Timestamp when the task was last modified")

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Task"
        verbose_name_plural = "Tasks"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("task_detail", kwargs={"pk": self.pk})


class TaskFile(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="files", help_text="The task this file belongs to")
    file = models.FileField("file", upload_to="task_files/", help_text="Upload a file (max 4 per task)")
    name = models.CharField("name", max_length=255, blank=True, help_text="Optional display name for the file")
    uploaded_at = models.DateTimeField(auto_now_add=True, help_text="Timestamp when the file was uploaded")

    class Meta:
        ordering = ["uploaded_at"]
        verbose_name = "Task File"
        verbose_name_plural = "Task Files"

    def __str__(self):
        return self.name or self.file.name

    def filename(self):
        return self.file.name.split("/")[-1]


class ContactMessage(models.Model):
    """User-submitted contact form message."""

    name = models.CharField("name", max_length=200, help_text="Your full name (required)")
    email = models.EmailField("email", help_text="Your email address so we can reply")
    message = models.TextField("message", help_text="How can we help you?")
    created_at = models.DateTimeField(auto_now_add=True, help_text="Timestamp when the message was submitted")

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Contact Message"
        verbose_name_plural = "Contact Messages"

    def __str__(self):
        return f"{self.name} - {self.email}"
