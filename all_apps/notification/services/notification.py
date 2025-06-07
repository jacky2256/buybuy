from typing import Type, Dict
from ..models import ChannelType, NotificationTemplate, TriggerEvent, TriggeredByType
from .strategies import (NotificationStrategy, EmailNotificationStrategy, SMSNotificationStrategy,
                         AppNotificationStrategy)


class NotificationService:
    _strategies: Dict[Type[ChannelType], Type[NotificationStrategy]] = {
        ChannelType.APP: AppNotificationStrategy,
        ChannelType.SMS: SMSNotificationStrategy,
        ChannelType.EMAIL: EmailNotificationStrategy,
    }

    @classmethod
    async def get_strategy(cls, instance: NotificationTemplate) -> NotificationStrategy:
        try:
            channel = ChannelType[instance.channel]
            strategy = cls._strategies[channel]
        except KeyError:
            raise Exception(f"Unknown notification strategy {instance.channel}")
        return strategy()
    
    @classmethod
    async def notify(
        cls,
        user,
        event: TriggerEvent,
        payload: dict
    ):
        content, _ = await NotificationTemplate.objects.aget_or_create(
            trigger_event=event,
            triggered_by=TriggeredByType.SYSTEM,
            defaults={
                "title": 'Default Title',
                "template": "This is a system notification.",
            },
        )
        strategy = await cls.get_strategy(content)
        return await strategy.send(user, content, payload)

