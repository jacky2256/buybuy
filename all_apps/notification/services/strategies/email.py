import logging
from .abstract import NotificationStrategy
from ...models import EmailNotification, StatusType


logger = logging.getLogger('django')

class EmailNotificationStrategy(NotificationStrategy):
    async def send(self, user, content, payload):
        notification = await EmailNotification.objects.acreate(user=user, content=content, payload=payload)
        try:
            await self._send_email(user.email, content.title, notification.email_content)
            notification.status = StatusType.SUCCESS
        except Exception as err:
            notification.status = StatusType.FAILED
            notification.status_reason = str(err)
        await notification.asave()

    async def _send_email(self, to_email, subject, body):
        logger.info(f"Sending email to {to_email} with subject {subject}")
        if "@" not in to_email:
            raise ValueError("Invalid email address")

