from django.utils import timezone


def get_default_datetime():
    dt = timezone.now()
    dt += timezone.timedelta(hours=2, minutes=-dt.minute, seconds=-dt.second, microseconds=-dt.microsecond)
    return dt

MONTH_CHOICES = (
    (1, 'january'),
    (2, 'february'),
    (3, 'march'),
    (4, 'april'),
    (5, 'may'),
    (6, 'august'),
    (7, 'june'),
    (8, 'july'),
    (9, 'september'),
    (10, 'october'),
    (11, 'november'),
    (12, 'december')
)