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


class WeekDay:
    def __init__(self, date, activities):
        self.date = date
        self.activities = activities

    @property
    def get_week_day_name(self):
        return self.date.strftime('%A')

def get_default_time(hours_shift=0):
    t = timezone.now()
    t += timezone.timedelta(hours=hours_shift, minutes=-t.minute, seconds=-t.second, microseconds=-t.microsecond)
    return t.astimezone(timezone.get_default_timezone()).time()


# TODO: clean this
# class Day:
#     def __init__(self, name, date=None, activities=None):
#         self.name = name
#         self.date = date
#         self.activities = activities
#
#     @property
#     def get_week_day_name_from_date(self):
#         return self.date.strftime('%A')
#
#
# def is_there_day_with_specified_date(days, date):
#     for day in days:
#         if day.date == date:
#             return True
#     return False
#
#
# def get_day_by_date(days, date):
#     """
#     Returns day with specified date if exist and None if not
#     :param days: list of days
#     :param date: date of day
#     :return:
#     """
#     for day in days:
#         if day.date == date:
#             return day
#     return None

# # List of Days with activity set
# days = []
# # Date of activities happening in ONE day
# day_activities_date = activities[0].date
# # List of activities happening in ONE day
# current_day_activities = []
#
# # Create list of Days with activity set
# for act in activities:
#     if act.date != day_activities_date:
#         days.append(Day(name=day_activities_date.strftime('%A'),
#                         date=day_activities_date,
#                         activities=current_day_activities))
#         current_day_activities = []
#
#         day_activities_date = act.date
#
#     elif act == activities.last():
#         days.append(Day(name=day_activities_date.strftime('%A'),
#                         date=day_activities_date,
#                         activities=current_day_activities))
#     # Add activity to the Day only if it's active
#     if act.status_active:
#         current_day_activities.append(act)
#
# new_days = []
#
# # Add activity to other Days if it's set to repeat weekly
# for day in days:
#     for act in day.activities:
#         if act.repeat_weekly:
#             other_monday_exist = False
#             for other_day in days:
#                 if other_day == day:
#                     continue
#                 # Add activity to other day if it is the same day in a week (eg both days are Mondays)
#                 if other_day.get_week_day_name_from_date == act.get_week_day_name:
#                     i = 0
#                     # Add activity in a proper place to save the proper ordering (by time_start)
#                     for o_act in other_day.activities:
#                         if act.time_start <= o_act.time_start:
#                             day.activities.insert(i, act)
#                             other_monday_exist = True
#                         i += 1
#             if not other_monday_exist:
#                 print('appending new day')
#                 new_days.append(Day(name=act.get_week_day_name, date=act.date, activities=[act]))
#
# print(days)
# for day in new_days:
#     days.append(day)
# print(days)
#
# # Date from form
# date = form.cleaned_data['date']
#
# # Date of Monday in a week in which selected day occurs
# week_monday_date = None
#
# # Get date of Monday in a week in which selected day occurs
# # week_day[0] is week day name
# # week_day[1] is week day index - Monday is 0, Sunday is 6
# for week_day in WEEK_DAYS:
#     if week_day[0] == date.strftime('%A'):
#         week_monday_date = date - timezone.timedelta(days=week_day[1])
#         break
#
# # List of Days which occurs in selected week
# week_days = []
#
# # List of week day names
# week_day_names = []
# for name in WEEK_DAYS:
#     week_day_names.append(name[0])
#
# # week_day_dates = []
# # for i in range(0, 7):
# #     week_day_dates.append(week_monday_date + timezone.timedelta(days=i))
# #
# # for day in days:
# #     if day.date in week_day_dates:
# #         week_days.append(day)
# #
# # for
#
# # Add Days to our week day list
# date = week_monday_date
# got_at_least_one_activity = False
# for i in range(0, 7):
#     day = get_day_by_date(days=days, date=date)
#     if day:
#         # Add Day from our list which occurs in selected week
#         week_days.append(day)
#         got_at_least_one_activity = True
#     else:
#         # Add Day with no activities for proper work of our template
#         week_days.append(Day(name=week_day_names[i], date=date))
#     date += timezone.timedelta(days=1)
#
# context = {'form': form}
#
# if got_at_least_one_activity:
#     context['week_days'] = week_days

# fresh start