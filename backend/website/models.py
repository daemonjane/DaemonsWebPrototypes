from django.db import models


class Task(models.Model):
    title = models.CharField("title", max_length=200)
    description = models.TextField("description", blank=True)
    completed = models.BooleanField("completed", default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Task"
        verbose_name_plural = "Tasks"

    def __str__(self):
        return self.title


class ContactMessage(models.Model):
    name = models.CharField("name", max_length=200)
    email = models.EmailField("email")
    message = models.TextField("message")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Contact Message"
        verbose_name_plural = "Contact Messages"

    def __str__(self):
        return f"{self.name} - {self.email}"
