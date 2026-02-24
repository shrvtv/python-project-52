from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse


class UserViewTestCase(TestCase):
    def create_users(self):
        self.user1 = User.objects.create_user(
            username="testuser1", 
            first_name="John", 
            last_name="Doe",
            password="testpassword1",
        )
        self.user2 = User.objects.create_user(
            username="testuser2",
            first_name="Jane",
            last_name="Smith",
            password="testpassword2",
        )
    
    def login_as_user1(self):
        self.client.login(
            username=self.user1.username, password="testpassword1"
        )


class UserListViewTests(UserViewTestCase):
    def setUp(self):
        self.create_users()
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


class UserCreateViewTests(UserViewTestCase):
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
            "password1": "testpassword1",
            "password2": "testpassword1",
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
            "password2": "",
        }
        response = self.client.post(self.url, invalid_form_data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username="testuser1").exists())


class UserUpdateViewTests(UserViewTestCase):
    def setUp(self):
        self.create_users()
        self.url = reverse("users:update", kwargs={"pk": self.user1.pk})

    def test_login_required(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertIn("login", response.url)

    def test_uses_correct_template(self):
        self.login_as_user1()
        response = self.client.get(self.url)
        
        self.assertTemplateUsed(response, "task_manager/users/form.html")

    def test_shows_correct_header(self):
        self.login_as_user1()
        response = self.client.get(self.url)
        self.assertContains(response, "Edit user")
        self.assertNotContains(response, "Registration")

    def test_shows_correct_button_label(self):
        self.login_as_user1()
        response = self.client.get(self.url)
        self.assertContains(response, "Modify")
        self.assertNotContains(response, "Sign up")

    def test_can_update_user(self):
        self.login_as_user1()
        updated_form_data = {
            "username": "testuser3",
            "first_name": "Mary",
            "last_name": "Sue",
            "password1": "testpassword3",
            "password2": "testpassword3",
        }
        response = self.client.post(self.url, updated_form_data)
        self.assertEqual(response.status_code, 302)
        self.user1.refresh_from_db()
        self.assertEqual(self.user1.username, "testuser3")
        self.assertEqual(self.user1.first_name, "Mary")
        self.assertEqual(self.user1.last_name, "Sue")
        self.assertRedirects(response, reverse("users:list"))

    def test_user_can_update_only_self(self):
        self.client.login(username="testuser1", password="testpassword1")
        url = reverse("users:update", kwargs={"pk": self.user2.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)


class UserDeleteViewTests(UserViewTestCase):
    def setUp(self):
        self.create_users()
        self.user_url = reverse(
            "users:delete", kwargs={"pk": self.user1.pk}
        )
        self.user_pk = self.user1.pk
        self.other_user_url = reverse(
            "users:delete", kwargs={"pk": self.user2.pk}
        )

    def test_login_required(self):
        response = self.client.get(self.user_url)
        self.assertEqual(response.status_code, 302)
        self.assertIn("login", response.url)

    def test_view_uses_correct_template(self):
        self.login_as_user1()
        response = self.client.get(self.user_url)
        self.assertTemplateUsed(response, "task_manager/users/delete.html")

    def test_can_delete_user(self):
        self.login_as_user1()
        response = self.client.post(self.user_url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(User.objects.filter(pk=self.user_pk).exists())
        self.assertRedirects(response, reverse("index"))

    def test_user_can_delete_only_self(self):
        self.login_as_user1()
        response = self.client.get(self.other_user_url)
        self.assertEqual(response.status_code, 403)
