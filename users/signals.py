from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Profile
from .tasks import send_welcome_mail

User = get_user_model()


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created and instance.email:
        Profile.objects.create(user=instance, nick_name=instance.username)


@receiver(post_save, sender=User)
def send_welcome(sender, instance, created, **kwargs):
    if created:
        send_welcome_mail.delay(instance.id)


@receiver(pre_save, sender=User)
def set_unique_username(sender, instance, **kwargs):
    if not instance.username and instance.email:
        base_username = instance.email.split('@')[0]
        username = base_username
        counter = 1

        # Ensure uniqueness
        while User.objects.filter(username=username).exclude(pk=instance.pk).exists():
            username = f"{base_username}{counter}"
            counter += 1

        instance.username = username
