import re

from django.db import models


class ChannelType(models.TextChoices):
    APP = 'APP', 'IN-App Notification'
    SMS = 'SMS', 'SMS'
    EMAIL = 'EMAIL', 'Email'


class TriggerEvent(models.TextChoices):
    ENROLMENT = 'ENROLMENT', 'Enrollment'
    ANNOUNCEMENT = 'ANNOUNCEMENT', 'Announcement'
    PROMOTIONAL = 'PROMOTIONAL', 'Promotional'
    RESET_PASSWORD = 'RESET_PASSWORD', 'Reset Password'


class TriggeredByType(models.TextChoices):
    SYSTEM = 'SYSTEM', 'System Notification'
    ADMIN = 'ADMIN', 'Admin Notification'


class StatusType(models.TextChoices):
    PENDING = 'PENDING', 'Pending'
    SUCCESS = 'SUCCESS', 'Success'
    FAILED = 'FAILED', 'Failed'


class NotificationTemplate(models.Model):
    title = models.CharField(max_length=255)
    template = models.TextField(help_text='Use placeholders like {{ username }} for personalization.')
    channel = models.CharField(max_length=20, choices=ChannelType.choices, default=ChannelType.APP)
    triggered_by = models.CharField(max_length=20, choices=TriggeredByType.choices, default=TriggeredByType.SYSTEM)
    trigger_event = models.CharField(max_length=20, choices=TriggerEvent.choices, default=TriggerEvent.ENROLMENT)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Notification(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='notifications')
    content = models.ForeignKey('notification.NotificationTemplate', on_delete=models.CASCADE, related_name='notifications')
    payload = models.JSONField(default=dict, help_text="Data to replace template placeholders.")
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


class EmailNotification(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='email_notifications')
    content = models.ForeignKey('notification.NotificationTemplate', on_delete=models.CASCADE, related_name='email_notifications')
    payload = models.JSONField(default=dict)
    status = models.CharField(max_length=20, choices=StatusType.choices, default=StatusType.PENDING)
    status_reason = models.TextField(null=True)

    @property
    def email_content(self):
        """
        Populate the template with dynamic data from payload.
        """
        content = self.content.template
        for key, value in self.payload.items():
            content = re.sub(
                rf"{{{{\s*{key}\s*}}}}",
                str(value),
                content,
            )
        return content


class SMSNotification(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='sms_notifications')
    content = models.ForeignKey('notification.NotificationTemplate', on_delete=models.CASCADE, related_name='sms_notifications')
    payload = models.JSONField(default=dict)
    status = models.CharField(max_length=20, choices=StatusType.choices, default=StatusType.PENDING)
    status_reason = models.TextField(null=True)

    @property
    def email_content(self):
        """
        Populate the template with dynamic data from payload.
        """
        content = self.content.template
        for key, value in self.payload.items():
            content = re.sub(
                rf"{{{{\s*{key}\s*}}}}",
                str(value),
                content,
            )
        return content



