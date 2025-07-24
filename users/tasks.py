from .models import Friend
from celery import shared_task
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.conf import settings
from django.utils import timezone
from datetime import timedelta


@shared_task
def send_welcome_mail(user_pk):
    user = User.objects.filter(id=user_pk).first()

    send_mail(
        subject='Welcome to MyApp!',
        message='Thank you for joining MyApp. We’re excited to have you!',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
    )

    return f"mail sended to email {user.email}"


@shared_task
def delete_old_rejected_requests():
    time = timezone.now() - timedelta(days=2)
    requests = Friend.objects.filter(created_at__lt=time)
    delete_count, _ = requests.delete()

    return f"Deleted {delete_count} Requests"
