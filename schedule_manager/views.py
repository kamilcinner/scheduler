from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.utils import timezone
from django.shortcuts import render
from django.views import generic

from schedule_manager.forms import ScheduleWeekSelectForm, ActivityCreateModelForm
from schedule_manager.models import Activity#, ScheduledDay
from schedule_manager.utils import *


# @login_required
# def schedule_week_detail_view(request):
#     if request.method == 'POST':
#         form = ScheduleWeekSelectForm(request.POST)
#         if form.is_valid():
#             scheduled_days = ScheduledDay.objects.filter(owner__username__exact=request.user.username)
#             date = timezone.datetime(year=int(form.cleaned_data['year']), month=int(form.cleaned_data['month']), day=int(form.cleaned_data['day']))
#             selected_day = None
#             week_first_obtainable_day = None
#
#             for day in scheduled_days:
#                 if day.date == date.date():
#                     selected_day = day
#                     break
#
#             # Get date of first day in a week
#             for week_day in WEEK_DAYS:
#                 if week_day[0] == selected_day.date.strftime('%A'):
#                     week_first_obtainable_day = selected_day.date - timezone.timedelta(days=week_day[1])
#                     break
#
#             got_first_day = False
#             week_days = []
#             week_day_names = []
#             for name in WEEK_DAYS:
#                 week_day_names.append(name[0])
#             day_number = 0
#             while not scheduled_days.filter(date__exact=week_first_obtainable_day).exists():
#                 week_first_obtainable_day += timezone.timedelta(days=1)
#                 week_days.append(WeekDay(week_day_names[day_number]))
#                 day_number += 1
#             for day in scheduled_days:
#                 if day.date == week_first_obtainable_day:
#                     got_first_day = True
#                 if got_first_day:
#                     week_days.append(WeekDay(week_day_names[day_number], day))
#                     day_number += 1
#                     if day_number == 7:
#                         break
#
#             context = {
#                 'form': form,
#                 'week_days': week_days
#             }
#
#             return render(request, 'schedule_manager/scheduleweek.html', context=context)
#
#     form = ScheduleWeekSelectForm()
#     context = {'form': form}
#     return render(request, 'schedule_manager/scheduleweek.html', context=context)





@login_required
def schedule_week_detail_view(request):
    if request.method == 'POST':
        form = ScheduleWeekSelectForm(request.POST)
        activities = Activity.objects.filter(owner__username__exact=request.user.username)
        if form.is_valid() and activities:
            # scheduled_days = []
            days = []
            # Date of activities happening in ONE day
            day_activities_date = activities[0].date
            # Create first date based on activities
            current_day = Day(day_activities_date.strftime('%A'), day_activities_date, [])

            # Create list of Days with activity set
            for act in activities:
                if act.date != day_activities_date:
                    days.append(current_day)

                    day_activities_date = act.date

                    current_day.name = day_activities_date.strftime('%A')
                    current_day.date = day_activities_date
                    current_day.activities.clear()
                elif act == activities.last():
                    days.append(current_day)

                current_day.activities.append(act)

            # Date from form
            date = timezone.datetime(year=int(form.cleaned_data['year']), month=int(form.cleaned_data['month']), day=int(form.cleaned_data['day'])).date()
            # Day with date from form
            selected_day = None
            # Date of first obtainable day in a week in which selected_day occurs
            week_first_obtainable_day = None

            # Get day with date from form
            for day in days:
                if day.date == date:
                    selected_day = day
                    break

            # Get date of Monday in a week in which selected_day occurs
            # week_day[0] is week day name
            # week_day[1] is week day index - Monday is 0, Sunday is 6
            for week_day in WEEK_DAYS:
                if week_day[0] == selected_day.name:
                    week_first_obtainable_day = selected_day.date - timezone.timedelta(days=week_day[1])
                    break

            # List of Days which occurs in selected week
            week_days = []
            
            # List of week day names
            week_day_names = []
            for name in WEEK_DAYS:
                week_day_names.append(name[0])

            # Number of Day in a week - Monday is 0
            day_number = 0

            # Check if there are some days before first obtainable day that is declared
            # Check if Monday is not obtainable and if so, then change day to Tuesday and check again
            # Obtainable means that we really want it to be Monday, but if first obtainable day is Wednesday, then we have to start with it
            while not is_there_day_with_specified_date(days, week_first_obtainable_day):
                # Add Day with no activities for proper work of our template
                week_days.append(Day(name=week_day_names[day_number], date=week_first_obtainable_day))
                week_first_obtainable_day += timezone.timedelta(days=1)
                day_number += 1

            got_first_day = False

            for day in days:
                if day.date == week_first_obtainable_day:
                    got_first_day = True
                if got_first_day:
                    week_days.append(day)
                    day_number += 1
                    if day_number >= 7:
                        break

            # Add empty Days with no activities
            while day_number < 7:
                week_days.append(Day(week_day_names[day_number]))
                day_number += 1

            context = {
                'form': form,
                'week_days': week_days
            }

            return render(request, 'schedule_manager/scheduleweek.html', context=context)

    form = ScheduleWeekSelectForm()
    context = {'form': form}
    return render(request, 'schedule_manager/scheduleweek.html', context=context)


class ActivityCreateModelView(generic.CreateView):
    model = Activity
    form_class = ActivityCreateModelForm

    def form_valid(self, form):
        """
        Add user to form data before setting it as valid (so it is saved to model)
        """
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('schedule_manager:activity-create')
