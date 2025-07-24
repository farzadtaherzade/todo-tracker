from django.core.management.base import BaseCommand
from django_celery_beat.models import PeriodicTask, CrontabSchedule, IntervalSchedule


class Command(BaseCommand):
    help = 'Setup periodic task to delete old rejected requests'

    def handle(self, *args, **options):
        schedule, _ = CrontabSchedule.objects.get_or_create(
            minute='0',
            hour='0',
            day_of_month='*/2',
            month_of_year='*',
            day_of_week='*',
        )

        deadline_schedule, _ = IntervalSchedule.objects.get_or_create(
            every=60,
            period=IntervalSchedule.SECONDS
        )

        PeriodicTask.objects.update_or_create(
            name='Delete old rejected requests every 2 days',
            defaults={
                'crontab': schedule,
                'task': 'users.tasks.delete_old_rejected_requests',
            }
        )

        PeriodicTask.objects.update_or_create(
            interval=deadline_schedule,
            name="Send and Update todo deadline to user and the watcher",
            task="todo.tasks.send_deadline_notification"
        )
        self.stdout.write(self.style.SUCCESS(
            'Successfully set up periodic task.'))
