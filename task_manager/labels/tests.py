from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from task_manager.labels.models import Label


class LabelViewTestCase(TestCase):
    def create_label(self, name="testlabel1"):
        return Label.objects.create(
            name=name,
        )

    def login_as_user(self):
        self.user = User.objects.create_user(
            username="testuser1", 
            first_name="John", 
            last_name="Doe",
            password="testpassword1",
        )
        self.client.login(username="testuser1", password="testpassword1")


class LabelViewRedirectTest(LabelViewTestCase):
    def make_redirect_url(self, url):
        return f"{reverse('login')}?next={url}"

    def setUp(self):
        self.label = self.create_label()

    def test_list(self):
        url = reverse("labels:list")
        self.assertRedirects(
            self.client.get(url),
            self.make_redirect_url(url)
        )
    
    def test_create(self):
        url = reverse("labels:create")
        self.assertRedirects(
            self.client.get(url),
            self.make_redirect_url(url)
        )

    def test_update(self):
        url = reverse("labels:update", args=[self.label.pk])
        self.assertRedirects(
            self.client.get(url),
            self.make_redirect_url(url)
        )

    def test_delete(self):
        url = reverse("labels:delete", args=[self.label.pk])
        self.assertRedirects(
            self.client.get(url),
            self.make_redirect_url(url)
        )


class LabelListViewTests(LabelViewTestCase):
    def setUp(self):
        self.label = self.create_label()
        self.login_as_user()
        self.response = self.client.get(reverse("labels:list"))

    def test_url_exists(self):
        self.assertEqual(self.response.status_code, 200)

    def test_uses_correct_template(self):
        self.assertTemplateUsed(self.response, "task_manager/labels/list.html")

    def test_shows_labels(self):
        self.assertContains(self.response, "testlabel1")

    def test_shows_multiple_labels(self):
        self.create_label(name="testlabel2")
        response = self.client.get(reverse("labels:list"))
        self.assertContains(response, "testlabel1")
        self.assertContains(response, "testlabel2")


class LabelCreateViewTests(LabelViewTestCase):
    def setUp(self):
        self.url = reverse("labels:create")
        self.label = self.create_label()
        self.login_as_user()
        self.response_get = self.client.get(self.url)

    def test_url_exists_when_logged_in(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_uses_correct_template(self):
        self.assertTemplateUsed(self.response_get, "task_manager/labels/form.html")

    def test_uses_correct_header(self):
        self.assertContains(self.response_get, "Create label")
        self.assertNotContains(self.response_get, "Edit label")

    def test_uses_correct_button_label(self):
        self.assertContains(self.response_get, "Create")
        self.assertNotContains(self.response_get, "Edit")

    def test_can_create_label(self):
        valid_form_data = {
            "name": "newlabel",
        }
        response = self.client.post(self.url, valid_form_data)
        self.assertRedirects(response, reverse("labels:list"))
        self.assertTrue(Label.objects.filter(name="newlabel").exists())

    def test_name_validation_works(self):
        invalid_form_data = {
            "name": "",
        }
        response = self.client.post(self.url, invalid_form_data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Label.objects.filter(name="").exists())


class LabelUpdateViewTests(LabelViewTestCase):
    def setUp(self):
        self.label = self.create_label()
        self.login_as_user()
        self.url = reverse("labels:update", kwargs={"pk": self.label.pk})

    def test_uses_correct_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "task_manager/labels/form.html")

    def test_shows_correct_header(self):
        response = self.client.get(self.url)
        self.assertContains(response, "Edit label")
        self.assertNotContains(response, "Create label")

    def test_shows_correct_button_label(self):
        response = self.client.get(self.url)
        self.assertContains(response, "Edit")
        self.assertNotContains(response, "Create")

    def test_can_update_label(self):
        updated_form_data = {
            "name": "updatedlabel",
        }
        response = self.client.post(self.url, updated_form_data)
        self.label.refresh_from_db()
        self.assertEqual(self.label.name, "updatedlabel")
        self.assertRedirects(response, reverse("labels:list"))


class LabelDeleteViewTests(LabelViewTestCase):
    def setUp(self):
        self.label = self.create_label()
        self.login_as_user()
        self.label_url = reverse("labels:delete", kwargs={"pk": self.label.pk})

    def test_view_uses_correct_template(self):
        response = self.client.get(self.label_url)
        self.assertTemplateUsed(response, "task_manager/labels/delete.html")

    def test_can_delete_label(self):
        response = self.client.post(self.label_url)
        self.assertFalse(Label.objects.filter(pk=self.label.pk).exists())
        self.assertRedirects(response, reverse("labels:list"))
