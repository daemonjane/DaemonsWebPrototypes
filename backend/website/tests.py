from django.test import TestCase
from django.urls import reverse

from .models import Task


class TaskModelTests(TestCase):
    def test_create_task(self):
        task = Task.objects.create(title="Test Task")
        self.assertEqual(str(task), "Test Task")
        self.assertFalse(task.completed)

    def test_task_absolute_url(self):
        task = Task.objects.create(title="Test")
        self.assertEqual(task.get_absolute_url(), f"/tasks/{task.pk}/")

    def test_task_default_completed(self):
        task = Task.objects.create(title="Test")
        self.assertFalse(task.completed)

    def test_task_ordering(self):
        Task.objects.all().delete()
        a = Task.objects.create(title="First")
        b = Task.objects.create(title="Second")
        tasks = Task.objects.all()
        self.assertEqual(tasks[0], b)
        self.assertEqual(tasks[1], a)


class TaskViewTests(TestCase):
    def test_list_view(self):
        resp = self.client.get(reverse("task_list"))
        self.assertEqual(resp.status_code, 200)

    def test_create_view_get(self):
        resp = self.client.get(reverse("task_create"))
        self.assertEqual(resp.status_code, 200)

    def test_create_view_post(self):
        resp = self.client.post(reverse("task_create"), {"title": "New"})
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(Task.objects.count(), 1)


class ContactViewTests(TestCase):
    def test_contact_get(self):
        resp = self.client.get(reverse("contact"))
        self.assertEqual(resp.status_code, 200)

    def test_contact_post(self):
        resp = self.client.post(reverse("contact"), {
            "name": "Test", "email": "test@example.com", "message": "Hello"
        })
        self.assertEqual(resp.status_code, 302)
