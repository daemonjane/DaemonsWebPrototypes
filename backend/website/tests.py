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
    def setUp(self):
        from django.contrib.auth.models import User
        self.user = User.objects.create_user("testuser", password="testpass")
        self.client.login(username="testuser", password="testpass")

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

    def test_update_view_get(self):
        task = Task.objects.create(title="Test")
        resp = self.client.get(reverse("task_update", kwargs={"pk": task.pk}))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Edit Task")

    def test_update_view_post(self):
        task = Task.objects.create(title="Old")
        resp = self.client.post(reverse("task_update", kwargs={"pk": task.pk}), {"title": "New"})
        self.assertEqual(resp.status_code, 302)
        task.refresh_from_db()
        self.assertEqual(task.title, "New")

    def test_delete_view_get(self):
        task = Task.objects.create(title="Test")
        resp = self.client.get(reverse("task_delete", kwargs={"pk": task.pk}))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Delete Task")

    def test_delete_view_post(self):
        task = Task.objects.create(title="Test")
        resp = self.client.post(reverse("task_delete", kwargs={"pk": task.pk}))
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(Task.objects.count(), 0)

    def test_detail_view(self):
        task = Task.objects.create(title="Test")
        resp = self.client.get(reverse("task_detail", kwargs={"pk": task.pk}))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Test")

    def test_toggle_view_post(self):
        task = Task.objects.create(title="Test")
        resp = self.client.post(reverse("task_toggle", kwargs={"pk": task.pk}))
        self.assertEqual(resp.status_code, 302)
        task.refresh_from_db()
        self.assertTrue(task.completed)


class ContactViewTests(TestCase):
    def test_contact_get(self):
        resp = self.client.get(reverse("contact"))
        self.assertEqual(resp.status_code, 200)

    def test_contact_post(self):
        resp = self.client.post(reverse("contact"), {
            "name": "Test", "email": "test@example.com", "message": "Hello"
        })
        self.assertEqual(resp.status_code, 302)
