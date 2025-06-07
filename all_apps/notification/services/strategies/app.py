import logging
from .abstract import NotificationStrategy
from ...models import Notification

logger = logging.getLogger(__name__)


class AppNotificationStrategy(NotificationStrategy):
    async def send(self, user, content, payload):
        notification = Notification.objects.acreate(user=user, content=content, payload=payload)
        logger.info(f"Notification sent to {user.email}: {content}")
        return notification
