from django.utils import timezone


def get_default_datetime():
    dt = timezone.now()
    dt += timezone.timedelta(hours=2, minutes=-dt.minute, seconds=-dt.second, microseconds=-dt.microsecond)
    return dt
