from django.contrib import admin

from schedule_manager.models import ScheduledDay, Activity


admin.site.register(ScheduledDay)
admin.site.register(Activity)
