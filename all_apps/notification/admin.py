from django.contrib import admin
from .models import NotificationTemplate

@admin.register(NotificationTemplate)
class NotificationTemplateAdmin(admin.ModelAdmin):
    list_display = ('title', 'channel', 'triggered_by', 'trigger_event', 'is_active')
    list_filter = ('channel', 'triggered_by', 'is_active')
    search_fields = ('title', 'trigger_event')

