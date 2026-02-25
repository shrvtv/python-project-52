from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from task_manager.statuses.models import Status


class StatusViewTestCase(TestCase):
    def create_status(self):
        return Status.objects.create(
            name="teststatus1",
        )

    def login_as_user(self):
        self.user = User.objects.create_user(
            username="testuser1", 
            first_name="John", 
            last_name="Doe",
            password="testpassword1",
        )
        self.client.login(username="testuser1", password="testpassword1")



class StatusViewRedirectTest(StatusViewTestCase):
    def make_redirect_url(self, url):
        return f"{reverse('login')}?next={url}"

    def setUp(self):
        self.status = self.create_status()

    def test_list(self):
        url = reverse("statuses:list")
        self.assertRedirects(
            self.client.get(url),
            self.make_redirect_url(url)
        )
    
    def test_create(self):
        url = reverse("statuses:create")
        self.assertRedirects(
            self.client.get(url),
            self.make_redirect_url(url)
        )

    def test_update(self):
        url = reverse("statuses:update", args=[self.status.pk])
        self.assertRedirects(
            self.client.get(url),
            self.make_redirect_url(url)
        )

    def test_delete(self):
        url = reverse("statuses:delete", args=[self.status.pk])
        self.assertRedirects(
            self.client.get(url),
            self.make_redirect_url(url)
        )


class StatusListViewTests(StatusViewTestCase):
    def setUp(self):
        self.status = self.create_status()
        self.login_as_user()
        self.response = self.client.get(reverse("statuses:list"))

    def test_url_exists(self):
        self.assertEqual(self.response.status_code, 200)

    def test_uses_correct_template(self):
        self.assertTemplateUsed(self.response, "task_manager/statuses/list.html")

    def test_shows_statuses(self):
        self.assertContains(self.response, "teststatus1")


class StatusCreateViewTests(StatusViewTestCase):
    def setUp(self):
        self.url = reverse("statuses:create")
        self.status = self.create_status()
        self.login_as_user()
        self.response_get = self.client.get(self.url)

    def test_url_exists_when_logged_in(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_uses_correct_template(self):
        self.assertTemplateUsed(self.response_get, "task_manager/statuses/form.html")

    def test_uses_correct_header(self):
        self.assertContains(self.response_get, "Create status")
        self.assertNotContains(self.response_get, "Edit status")

    def test_uses_correct_button_label(self):
        self.assertContains(self.response_get, "Create")
        self.assertNotContains(self.response_get, "Edit")

    def test_can_create_status(self):
        valid_form_data = {
            "name": "newstatus",
        }
        response = self.client.post(self.url, valid_form_data)
        self.assertRedirects(response, reverse("statuses:list"))
        self.assertTrue(Status.objects.filter(name="newstatus").exists())

    def test_name_validation_works(self):
        invalid_form_data = {
            "name": "",
        }
        response = self.client.post(self.url, invalid_form_data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Status.objects.filter(name="").exists())


class StatusUpdateViewTests(StatusViewTestCase):
    def setUp(self):
        self.status = self.create_status()
        self.login_as_user()
        self.url = reverse("statuses:update", kwargs={"pk": self.status.pk})

    def test_uses_correct_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "task_manager/statuses/form.html")

    def test_shows_correct_header(self):
        response = self.client.get(self.url)
        self.assertContains(response, "Edit status")
        self.assertNotContains(response, "Create status")

    def test_shows_correct_button_label(self):
        response = self.client.get(self.url)
        self.assertContains(response, "Edit")
        self.assertNotContains(response, "Create")

    def test_can_update_status(self):
        updated_form_data = {
            "name": "updatedstatus",
        }
        response = self.client.post(self.url, updated_form_data)
        self.status.refresh_from_db()
        self.assertEqual(self.status.name, "updatedstatus")
        self.assertRedirects(response, reverse("statuses:list"))


class StatusDeleteViewTests(StatusViewTestCase):
    def setUp(self):
        self.status = self.create_status()
        self.login_as_user()
        self.status_url = reverse("statuses:delete", kwargs={"pk": self.status.pk})

    def test_view_uses_correct_template(self):
        response = self.client.get(self.status_url)
        self.assertTemplateUsed(response, "task_manager/statuses/delete.html")

    def test_can_delete_status(self):
        response = self.client.post(self.status_url)
        self.assertFalse(Status.objects.filter(pk=self.status.pk).exists())
        self.assertRedirects(response, reverse("statuses:list"))
