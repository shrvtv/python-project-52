from django.test import TestCase
from django.urls import reverse

from task_manager.statuses.models import Status
from task_manager.tasks.models import Task


class TaskViewTestCase(TestCase):
    fixtures = ["users.json", "statuses.json", "labels.json", "tasks.json"]

    def setUp(self):
        self.task = Task.objects.get(pk=1)
        self.status = Status.objects.get(pk=1)

    def login_as_user(self):
        self.client.login(username="testuser1", password="testpassword1")


class TaskViewRedirectTest(TaskViewTestCase):
    def setUp(self):
        super().setUp()

    def make_redirect_url(self, url):
        return f"{reverse('login')}?next={url}"

    def test_list(self):
        url = reverse("tasks:list")
        self.assertRedirects(self.client.get(url), self.make_redirect_url(url))

    def test_create(self):
        url = reverse("tasks:create")
        self.assertRedirects(self.client.get(url), self.make_redirect_url(url))

    def test_view(self):
        url = reverse("tasks:view", args=[self.task.pk])
        self.assertRedirects(self.client.get(url), self.make_redirect_url(url))

    def test_update(self):
        url = reverse("tasks:update", args=[self.task.pk])
        self.assertRedirects(self.client.get(url), self.make_redirect_url(url))

    def test_delete(self):
        url = reverse("tasks:delete", args=[self.task.pk])
        self.assertRedirects(self.client.get(url), self.make_redirect_url(url))


class TaskListViewTests(TaskViewTestCase):
    def setUp(self):
        super().setUp()
        self.login_as_user()
        self.response = self.client.get(reverse("tasks:list"))

    def test_url_exists(self):
        self.assertEqual(self.response.status_code, 200)

    def test_uses_correct_template(self):
        self.assertTemplateUsed(self.response, "task_manager/tasks/list.html")

    def test_shows_tasks(self):
        self.assertContains(self.response, self.task.name)


class TaskCreateViewTests(TaskViewTestCase):
    def setUp(self):
        super().setUp()
        self.url = reverse("tasks:create")
        self.login_as_user()
        self.response_get = self.client.get(self.url)

    def test_url_exists_when_logged_in(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_uses_correct_template(self):
        self.assertTemplateUsed(self.response_get, "task_manager/tasks/form.html")

    def test_uses_correct_header(self):
        self.assertContains(self.response_get, "Create task")
        self.assertNotContains(self.response_get, "Edit task")

    def test_uses_correct_button_label(self):
        self.assertContains(self.response_get, "Create")
        self.assertNotContains(self.response_get, "Edit")

    def test_can_create_task(self):
        valid_form_data = {
            "name": "name2",
            "description": "description2",
            "status": self.status.pk,
        }
        response = self.client.post(self.url, valid_form_data)
        self.assertRedirects(response, reverse("tasks:list"))
        self.assertTrue(Task.objects.filter(name="name2").exists())

    def test_name_validation_works(self):
        invalid_form_data = {
            "name": "",
            "description": "",
            "status": self.status.pk,
        }
        response = self.client.post(self.url, invalid_form_data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Task.objects.filter(name="").exists())


class TaskUpdateViewTests(TaskViewTestCase):
    def setUp(self):
        super().setUp()
        self.login_as_user()
        self.url = reverse("tasks:update", kwargs={"pk": self.task.pk})

    def test_uses_correct_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "task_manager/tasks/form.html")

    def test_shows_correct_header(self):
        response = self.client.get(self.url)
        self.assertContains(response, "Edit task")
        self.assertNotContains(response, "Create task")

    def test_shows_correct_button_label(self):
        response = self.client.get(self.url)
        self.assertContains(response, "Edit")
        self.assertNotContains(response, "Create")

    def test_can_update_task(self):
        updated_form_data = {
            "name": "new name",
            "description": "new description",
            "status": self.status.pk,
        }
        response = self.client.post(self.url, updated_form_data)
        self.task.refresh_from_db()
        self.assertEqual(self.task.name, "new name")
        self.assertEqual(self.task.description, "new description")
        self.assertRedirects(response, reverse("tasks:list"))


class TaskDeleteViewTests(TaskViewTestCase):
    def setUp(self):
        super().setUp()
        self.login_as_user()
        self.task_url = reverse("tasks:delete", kwargs={"pk": self.task.pk})

    def test_view_uses_correct_template(self):
        response = self.client.get(self.task_url)
        self.assertTemplateUsed(response, "task_manager/tasks/delete.html")

    def test_can_delete_task(self):
        response = self.client.post(self.task_url)
        self.assertFalse(Task.objects.filter(pk=self.task.pk).exists())
        self.assertRedirects(response, reverse("tasks:list"))
