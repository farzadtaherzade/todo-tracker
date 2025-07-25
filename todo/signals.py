from .models import Todo
from django.core.mail import send_mail
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
from .tasks import notify_task_completed_to_watcher, send_watcher_notification_email


@receiver(post_save, sender=Todo)
def notif_user_assigned_watcher(sender, instance, created, **kwargs):
    if created and instance.watcher:
        watcher_email = instance.watcher.email
        send_watcher_notification_email.delay(
            watcher_email=instance.watcher.email,
            watcher_username=instance.watcher.username,
            todo_title=instance.title,
            owner_username=instance.user.username,
        )


@receiver(pre_save, sender=Todo)
def notif_watcher_todo_completed(sender, instance: Todo, **kwargs):
    try:
        old = Todo.objects.get(pk=instance.pk)
        if not old.is_completed and instance.is_completed and instance.watcher:
            notify_task_completed_to_watcher.delay(
                watcher_email=instance.watcher.email,
                watcher_username=instance.watcher.username,
                todo_title=instance.title,
                owner_username=instance.user.username,
            )
    except Todo.DoesNotExist:
        pass
