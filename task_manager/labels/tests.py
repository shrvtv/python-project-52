from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from task_manager.labels.models import Label


class StatusViewTestCase(TestCase):
    def create_label(self):
        return Label.objects.create(
            name="testlabel1",
        )

    def login_as_user(self):
        self.user = User.objects.create_user(
            username="testuser1", 
            first_name="John", 
            last_name="Doe",
            password="testpassword1",
        )
        self.client.login(username="testuser1", password="testpassword1")
