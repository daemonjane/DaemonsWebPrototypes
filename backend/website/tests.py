from django.test import TestCase
from django.urls import reverse

from .models import Comment, Task


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


class CommentModelTests(TestCase):
    def setUp(self):
        self.task = Task.objects.create(title="Commentable Task")

    def test_create_comment(self):
        comment = Comment.objects.create(task=self.task, author="Alice", body="Nice task!")
        self.assertEqual(str(comment), f"Alice on {self.task.title}")
        self.assertEqual(self.task.comments.count(), 1)

    def test_comment_ordering(self):
        c1 = Comment.objects.create(task=self.task, author="A", body="First")
        c2 = Comment.objects.create(task=self.task, author="B", body="Second")
        comments = self.task.comments.all()
        self.assertEqual(comments[0], c1)
        self.assertEqual(comments[1], c2)

    def test_cascade_delete(self):
        Comment.objects.create(task=self.task, author="A", body="Test")
        self.assertEqual(Comment.objects.count(), 1)
        self.task.delete()
        self.assertEqual(Comment.objects.count(), 0)


class CommentViewTests(TestCase):
    def setUp(self):
        from django.contrib.auth.models import User
        self.user = User.objects.create_user("testuser", password="testpass")
        self.client.login(username="testuser", password="testpass")
        self.task = Task.objects.create(title="Test Task")

    def test_detail_view_shows_comments(self):
        Comment.objects.create(task=self.task, author="Alice", body="Great work")
        resp = self.client.get(reverse("task_detail", kwargs={"pk": self.task.pk}))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Great work")
        self.assertContains(resp, "Alice")

    def test_add_comment_post(self):
        resp = self.client.post(reverse("add_comment", kwargs={"pk": self.task.pk}), {
            "author": "Bob", "body": "Nice comment"
        })
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(self.task.comments.count(), 1)
        self.assertEqual(self.task.comments.first().author, "Bob")

    def test_add_comment_requires_login(self):
        self.client.logout()
        resp = self.client.post(reverse("add_comment", kwargs={"pk": self.task.pk}), {
            "author": "Eve", "body": "Hack!"
        })
        self.assertRedirects(resp, f"{reverse('login')}?next={reverse('add_comment', kwargs={'pk': self.task.pk})}")
        self.assertEqual(self.task.comments.count(), 0)

    def test_comment_count_in_task_list(self):
        Comment.objects.create(task=self.task, author="A", body="X")
        Comment.objects.create(task=self.task, author="B", body="Y")
        resp = self.client.get(reverse("task_list"))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "2")


class DashboardViewTests(TestCase):
    def setUp(self):
        from django.contrib.auth.models import User
        self.staff = User.objects.create_user("staff", password="pass", is_staff=True)
        self.user = User.objects.create_user("user", password="pass")

    def test_dashboard_requires_staff(self):
        self.client.login(username="user", password="pass")
        resp = self.client.get(reverse("admin_dashboard"))
        self.assertEqual(resp.status_code, 302)

    def test_dashboard_loads_for_staff(self):
        self.client.login(username="staff", password="pass")
        resp = self.client.get(reverse("admin_dashboard"))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Dashboard")

    def test_dashboard_shows_counts(self):
        from .models import Task
        Task.objects.create(title="T1")
        Task.objects.create(title="T2")
        self.client.login(username="staff", password="pass")
        resp = self.client.get(reverse("admin_dashboard"))
        self.assertContains(resp, "2")
        self.assertContains(resp, "0")

    def test_dashboard_shows_recent_orders(self):
        self.client.login(username="staff", password="pass")
        resp = self.client.get(reverse("admin_dashboard"))
        self.assertEqual(resp.status_code, 200)


class ContactViewTests(TestCase):
    def test_contact_get(self):
        resp = self.client.get(reverse("contact"))
        self.assertEqual(resp.status_code, 200)

    def test_contact_post(self):
        resp = self.client.post(reverse("contact"), {
            "name": "Test", "email": "test@example.com", "message": "Hello"
        })
        self.assertEqual(resp.status_code, 302)


class RegisterViewTests(TestCase):
    def test_register_get(self):
        resp = self.client.get(reverse("register"))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Create Account")

    def test_register_post_success(self):
        resp = self.client.post(reverse("register"), {
            "username": "newuser",
            "email": "new@example.com",
            "password1": "Str0ng!Pass",
            "password2": "Str0ng!Pass",
        })
        self.assertRedirects(resp, reverse("task_list"))
        from django.contrib.auth.models import User
        self.assertTrue(User.objects.filter(username="newuser").exists())

    def test_register_auto_login(self):
        self.client.post(reverse("register"), {
            "username": "autouser",
            "email": "auto@example.com",
            "password1": "Str0ng!Pass",
            "password2": "Str0ng!Pass",
        })
        resp = self.client.get(reverse("task_list"))
        self.assertEqual(resp.status_code, 200)

    def test_register_password_mismatch(self):
        resp = self.client.post(reverse("register"), {
            "username": "baduser",
            "email": "bad@example.com",
            "password1": "Str0ng!Pass",
            "password2": "DifferentPass1",
        })
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "password")

    def test_register_duplicate_username(self):
        from django.contrib.auth.models import User
        User.objects.create_user("existing", password="Pass123!")
        resp = self.client.post(reverse("register"), {
            "username": "existing",
            "email": "dup@example.com",
            "password1": "Str0ng!Pass",
            "password2": "Str0ng!Pass",
        })
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "already exists")
