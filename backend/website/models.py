from django.db import models
from django.urls import reverse


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
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Task"
        verbose_name_plural = "Tasks"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("task_detail", kwargs={"pk": self.pk})


class ContactMessage(models.Model):
    """User-submitted contact form message."""

    name = models.CharField("name", max_length=200, help_text="Your full name")
    email = models.EmailField("email", help_text="Your email address so we can reply")
    message = models.TextField("message", help_text="How can we help you?")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Contact Message"
        verbose_name_plural = "Contact Messages"

    def __str__(self):
        return f"{self.name} - {self.email}"
