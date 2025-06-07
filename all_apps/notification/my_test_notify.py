import asyncio

import os
import django
os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE', 'core.settings'
)
# os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
django.setup()

from django.contrib.auth.models import User
from all_apps.notification.services import NotificationService
from all_apps.notification.models import TriggerEvent


async def test_notify():
    _email = "a.bojic76@gmail.com"
    user = await User.objects.aget(email=_email)
    service = NotificationService()
    await service.notify(
        user=user,
        event=TriggerEvent.ANNOUNCEMENT,
        payload={
            "username": user.username,
            "project_title": "BuyBuy Project!",
        }
    )


if __name__ == '__main__':
    asyncio.run(test_notify())

