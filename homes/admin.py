from django.contrib import admin
from .models import Inquiry

@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email', 'display_message', 'status', 'created_at_ist')
    list_filter = ('status', 'created_at')
    search_fields = ('name', 'email', 'phone', 'message')
    list_editable = ('status',)
    actions = ['mark_as_talked']

    def display_message(self, obj):
        return obj.message[:50] + '...' if len(obj.message) > 50 else obj.message
    display_message.short_description = 'Message Preview'

    def created_at_ist(self, obj):
        # Ensure timezone conversion if not already done by TIME_ZONE setting
        from django.utils import timezone
        if obj.created_at.tzinfo is None or obj.created_at.tzinfo.utcoffset(obj.created_at) is None:
            # If datetime is naive, assume UTC and convert to IST
            utc_dt = timezone.make_aware(obj.created_at, timezone.utc)
            return utc_dt.astimezone(timezone.get_current_timezone()).strftime('%Y-%m-%d %H:%M:%S IST')
        else:
            # If datetime is already timezone-aware, convert to IST
            return obj.created_at.astimezone(timezone.get_current_timezone()).strftime('%Y-%m-%d %H:%M:%S IST')
    created_at_ist.short_description = 'Submitted At (IST)'

    def mark_as_talked(self, request, queryset):
        updated = queryset.update(status='Talked')
        self.message_user(request, f'{updated} inquiries successfully marked as talked.', level=admin.messages.SUCCESS)
    mark_as_talked.short_description = 'Mark selected inquiries as Talked'
