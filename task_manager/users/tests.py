from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse


class UserListViewTests(TestCase):
    def setUp(self):
        User.objects.create_user(username="testuser1", first_name="John", last_name="Doe")
        User.objects.create_user(username="testuser2", first_name="Jane", last_name="Smith")
        self.response = self.client.get(reverse("users:list"))

    def test_url_exists(self):
        self.assertEqual(self.response.status_code, 200)

    def test_uses_correct_template(self):
        self.assertTemplateUsed(self.response, "task_manager/users/list.html")

    def test_shows_users(self):
        self.assertContains(self.response, "testuser1")
        self.assertContains(self.response, "John Doe")
        self.assertContains(self.response, "testuser2")
        self.assertContains(self.response, "Jane Smith")


class UserCreateViewTests(TestCase):
    def setUp(self):
        self.url = reverse("users:create")
        self.response_get = self.client.get(self.url)

    def test_url_exists(self):
        self.assertEqual(self.response_get.status_code, 200)

    def test_uses_correct_template(self):
        self.assertTemplateUsed(self.response_get, "task_manager/users/form.html")

    def test_uses_correct_header(self):
        self.assertContains(self.response_get, "Registration")
        self.assertNotContains(self.response_get, "Edit user")

    def test_uses_correct_button_label(self):
        self.assertContains(self.response_get, "Sign up")
        self.assertNotContains(self.response_get, "Modify")

    def test_can_create_user(self):
        valid_form_data = {
            "username": "testuser1",
            "first_name": "John",
            "last_name": "Doe",
            "password1": "testpassword",
            "password2": "testpassword"
        }
        response = self.client.post(self.url, valid_form_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("users:list"))
        self.assertTrue(User.objects.filter(username="testuser1").exists())
        

    def test_password_validation_works(self):
        invalid_form_data = {
            "username": "testuser1",
            "first_name": "John",
            "last_name": "Doe",
            "password1": "",
            "password2": ""
        }
        response = self.client.post(self.url, invalid_form_data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username="testuser1").exists())
