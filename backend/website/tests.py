from unittest.mock import patch

from django.core import mail
from django.test import TestCase
from django.urls import reverse

from .models import Comment, NewsletterSubscription, Task


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


class TaskListPaginationTests(TestCase):
    def setUp(self):
        from django.contrib.auth.models import User
        self.user = User.objects.create_user("testuser", password="testpass")
        self.client.login(username="testuser", password="testpass")
        Task.objects.all().delete()
        for i in range(25):
            Task.objects.create(title=f"Task {i+1}")

    def test_page_one_returns_first_ten(self):
        resp = self.client.get(reverse("task_list"))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Task 25")
        self.assertContains(resp, "Task 16")
        self.assertNotContains(resp, "Task 15")

    def test_page_two_returns_next_ten(self):
        resp = self.client.get(reverse("task_list"), {"page": 2})
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Task 15")
        self.assertContains(resp, "Task 6")
        self.assertNotContains(resp, "Task 25")

    def test_page_three_returns_last_five(self):
        resp = self.client.get(reverse("task_list"), {"page": 3})
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Task 5")
        self.assertContains(resp, "Task 1")
        self.assertNotContains(resp, "Task 25")

    def test_invalid_page_returns_first(self):
        resp = self.client.get(reverse("task_list"), {"page": "abc"})
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Task 25")

    def test_out_of_range_page_returns_last(self):
        resp = self.client.get(reverse("task_list"), {"page": 999})
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Task 1")

    def test_pagination_links_shown_when_many_tasks(self):
        resp = self.client.get(reverse("task_list"))
        self.assertContains(resp, "Page 1 of 3")

    def test_no_pagination_when_few_tasks(self):
        Task.objects.all().delete()
        Task.objects.create(title="Only Task")
        resp = self.client.get(reverse("task_list"))
        self.assertEqual(resp.status_code, 200)
        self.assertNotContains(resp, "Page 1 of")

    def test_pagination_context(self):
        resp = self.client.get(reverse("task_list"))
        self.assertIn("paginator", resp.context)
        self.assertIn("page_obj", resp.context)
        self.assertEqual(resp.context["paginator"].num_pages, 3)

    def test_search_returns_all_matches(self):
        resp = self.client.get(reverse("task_search"), {"q": "Task"})
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data["count"], 25)


class DashboardViewTests(TestCase):
    def setUp(self):
        from django.contrib.auth.models import User
        self.staff = User.objects.create_user("staff", password="pass", is_staff=True)
        self.superuser = User.objects.create_user("super", password="pass", is_staff=True, is_superuser=True)
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

    def test_admin_add_product_page_loads(self):
        self.client.login(username="super", password="pass")
        resp = self.client.get("/admin/api/product/add/")
        self.assertEqual(resp.status_code, 200)

    def test_admin_add_category_page_loads(self):
        self.client.login(username="super", password="pass")
        resp = self.client.get("/admin/api/category/add/")
        self.assertEqual(resp.status_code, 200)

    def test_admin_add_task_page_loads(self):
        self.client.login(username="super", password="pass")
        resp = self.client.get("/admin/website/task/add/")
        self.assertEqual(resp.status_code, 200)

    def test_admin_change_list_loads(self):
        self.client.login(username="super", password="pass")
        for path in ["/admin/api/product/", "/admin/api/category/", "/admin/api/order/",
                      "/admin/website/task/", "/admin/website/comment/",
                      "/admin/website/contactmessage/"]:
            resp = self.client.get(path)
            self.assertEqual(resp.status_code, 200, f"{path} returned {resp.status_code}")


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


class EmailTests(TestCase):
    def test_contact_auto_reply_sent(self):
        resp = self.client.post(reverse("contact"), {
            "name": "Alice",
            "email": "alice@example.com",
            "message": "I love your store!",
        })
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn("Thank you for contacting TechStore", mail.outbox[0].subject)
        self.assertIn("alice@example.com", mail.outbox[0].to)
        self.assertIn("I love your store!", mail.outbox[0].body)

    def test_contact_auto_reply_does_not_block_on_failure(self):
        with patch("website.views.send_contact_auto_reply", side_effect=Exception("SMTP down")):
            resp = self.client.post(reverse("contact"), {
                "name": "Bob",
                "email": "bob@example.com",
                "message": "Hello",
            })
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, reverse("contact"))


class NewsletterSubscriptionTests(TestCase):
    def test_subscribe_creates_subscription_and_sends_email(self):
        resp = self.client.post(reverse("newsletter_subscribe"), {"email": "new@example.com"})
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(NewsletterSubscription.objects.filter(email="new@example.com").exists())
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn("Welcome to the TechStore newsletter", mail.outbox[0].subject)
        self.assertIn("new@example.com", mail.outbox[0].to)

    def test_subscribe_duplicate_does_not_create_duplicate(self):
        NewsletterSubscription.objects.create(email="dup@example.com")
        resp = self.client.post(reverse("newsletter_subscribe"), {"email": "dup@example.com"})
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(NewsletterSubscription.objects.filter(email="dup@example.com").count(), 1)
        self.assertEqual(len(mail.outbox), 0)

    def test_subscribe_reactivates_inactive(self):
        sub = NewsletterSubscription.objects.create(email="old@example.com", active=False)
        resp = self.client.post(reverse("newsletter_subscribe"), {"email": "old@example.com"})
        self.assertEqual(resp.status_code, 302)
        sub.refresh_from_db()
        self.assertTrue(sub.active)
        self.assertEqual(len(mail.outbox), 1)

    def test_subscribe_without_email_returns_error(self):
        resp = self.client.post(reverse("newsletter_subscribe"), {"email": ""})
        self.assertEqual(resp.status_code, 302)

    def test_newsletter_subscription_model_str(self):
        sub = NewsletterSubscription.objects.create(email="test@example.com")
        self.assertEqual(str(sub), "test@example.com")
