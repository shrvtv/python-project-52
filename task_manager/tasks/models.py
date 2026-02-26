from django.db import models
from django.contrib.auth.models import User
from task_manager.statuses.models import Status

class Task(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.ForeignKey(
        Status,
        on_delete=models.RESTRICT,
        related_name="status"
    )
    author = models.ForeignKey(
        User,
        on_delete=models.RESTRICT,
        related_name="tasks_authored"
    )
    executor = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name="tasks_executing"
    )
