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


class Friend(models.Model):
    STATUS_CHOICES = (
        (1, "Pending"),
        (2, "Accepted"),
        (3, "Rejected")
    )

    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="send_requests")
    receiver = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="received_requests")
    status = models.BigIntegerField(choices=STATUS_CHOICES, default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("sender", "receiver")
