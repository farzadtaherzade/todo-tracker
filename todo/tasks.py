from .models import Todo
from celery import shared_task
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings


@shared_task
def send_deadline_notification():
    now = timezone.now()
    todos = Todo.objects.filter(dead_line__gte=now, is_completed=False)
    for todo in todos:
        send_deadline_email.delay(todo.pk)


@shared_task
def send_deadline_email(todo_pk):
    try:
        todo = Todo.objects.get(pk=todo_pk)
        subject = f"Deadline Reached for ToDo: {todo.title}"
        message = f"Dear User,\n\nThe deadline for the ToDo '{todo.title}' has been reached.\n\nDetails:\n- Description: {todo.description}\n- Deadline: {todo.deadline}\n\nPlease take appropriate action.\n\nBest regards,\nYour ToDo App"
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [todo.watcher.email, todo.owner.email]

        send_mail(
            subject=subject,
            message=message,
            from_email=from_email,
            recipient_list=recipient_list,
            fail_silently=False,
        )
    except Todo.DoesNotExist:
        return f"Todo with id -- {todo_pk} -- not does not exists"
