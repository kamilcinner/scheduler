from django.urls import reverse
from django.utils import timezone


WEEK_DAYS = (
    ('Monday',       0),
    ('Tuesday',      1),
    ('Wednesday',    2),
    ('Thursday',     3),
    ('Friday',       4),
    ('Saturday',     5),
    ('Sunday',       6)
)


class WeekDayActivityTask:
    def __init__(self, pk, name, description, time, priority=None):
        self.pk = pk
        self.name = name
        self.description = description
        self.time = time
        self.priority = priority

    def get_absolute_url(self):
        if self.priority:
            url_name = 'task_manager:task-detail'
        else:
            url_name = 'schedule_manager:activity-detail'

        return reverse(url_name, args=[str(self.pk)])


class WeekDay:
    def __init__(self, date, week_day_activity_task_list):
        self.date = date
        self.week_day_activity_task_list = week_day_activity_task_list

    @property
    def week_day_name(self):
        return self.date.strftime('%A')


def get_default_time(hours_shift=0):
    t = timezone.now()
    t += timezone.timedelta(hours=hours_shift, minutes=-t.minute, seconds=-t.second, microseconds=-t.microsecond)
    return t.astimezone(timezone.get_default_timezone()).time()
