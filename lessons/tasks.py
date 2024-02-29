from datetime import datetime, timedelta

from celery import shared_task
from django.utils import timezone

from users.models import User


@shared_task
def check_user_is_outdated():
    now = datetime.now()
    now = timezone.make_aware(now, timezone.get_current_timezone())
    for user in User.objects.all():
        if user.last_login:
            if now - user.last_login > timedelta(days=30):
                user.is_active = False
                user.save()
