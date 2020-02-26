WEEK_DAYS = (
    ('Monday',       0),
    ('Tuesday',      1),
    ('Wednesday',    2),
    ('Thursday',     3),
    ('Friday',       4),
    ('Saturday',     5),
    ('Sunday',       6)
)


# class WeekDay:
#     def __init__(self, name, scheduled_day=None):
#         self.name = name
#         self.scheduled_day = scheduled_day


class Day:
    def __init__(self, name, date=None, activities=None):
        self.name = name
        self.date = date
        self.activities = activities


def is_there_day_with_specified_date(days, date):
    for day in days:
        if day.date == date:
            return True
    return False