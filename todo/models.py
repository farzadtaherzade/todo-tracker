from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.

User = get_user_model()


class Todo(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=500)

    dead_line = models.DateTimeField(null=True, blank=True)
    is_completed = models.BooleanField(default=False)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="todos")
    photo = models.ImageField(
        upload_to='todo_photos/', null=True, blank=True, default='todo_photos')
    watcher = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="watching_todos", null=True,
        blank=True, help_text="A friends or a family member can watch you do your todo and approve!")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
