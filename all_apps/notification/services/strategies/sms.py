import logging
from .abstract import NotificationStrategy
from ...models import SMSNotification

logger = logging.getLogger(__name__)


class SMSNotificationStrategy(NotificationStrategy):
    async def send(self, user, content, payload):
        notification = await SMSNotification.objects.acreate(user=user, content=content, payload=payload)
        try:
            await self._send_sms(user.phone_number, notification.content)
            notification.status = SMSNotification.StatusType.SUCCESS
        except Exception as err:
            notification.status = SMSNotification.StatusType.FAILED
            notification.status_reason = str(err)
        await notification.asave()
        return notification

    async def _send_sms(self, phone_number: str, message: str):
        logger.info(f"Sending SMS to {phone_number} with message: {message}")
        if not phone_number.isdigit():
            raise ValueError("Invalid phone number")