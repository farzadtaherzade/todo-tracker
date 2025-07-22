from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.

User = get_user_model()


class Profile(models.Model):
    avatar = models.ImageField(upload_to="profile", null=True, blank=True)
    nick_name = models.CharField(null=True, blank=True, max_length=100)
    bio = models.TextField(null=True, blank=True, max_length=500)
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="profile", null=True, blank=True
    )

    def __str__(self):
        return f"{self.user.username} Profile"
