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


@shared_task
def send_watcher_notification_email(watcher_email, watcher_username, todo_title, todo_description):
    subject = '📌 You have been assigned to a new task!'
    message = (
        f'Hello {watcher_username},\n\n'
        f'You have been assigned to watch the following task:\n'
        f'Title: {todo_title}\n'
        f'Description: {todo_description}'
    )
    send_mail(
        subject=subject,
        message=message,
        from_email='noreply@yourapp.com',
        recipient_list=[watcher_email],
        fail_silently=True,
    )

    return f'You have been assigned to watch the following task:\n'


@shared_task
def notify_task_completed_to_watcher(watcher_email, watcher_username, todo_title, owner_username):
    subject = '✅ Task Completed — Please Review'
    message = (
        f"Hello {watcher_username},\n\n"
        f"The task titled \"{todo_title}\" was marked as completed by {owner_username}.\n"
        f"Please review and confirm the task if everything is correct.\n\n"
        f"Thank you!"
    )
    send_mail(
        subject=subject,
        message=message,
        from_email='noreply@yourapp.com',
        recipient_list=[watcher_email],
        fail_silently=True,
    )
