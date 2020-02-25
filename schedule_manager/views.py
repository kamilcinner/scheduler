from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.shortcuts import render

from schedule_manager.forms import ScheduleWeekSelectForm
from schedule_manager.models import ScheduledDay
from schedule_manager.utils import WEEK_DAYS


class WeekDay:
    def __init__(self, name, scheduled_day=None):
        self.name = name
        self.scheduled_day = scheduled_day


@login_required
def schedule_week_detail_view(request):
    if request.method == 'POST':
        form = ScheduleWeekSelectForm(request.POST)
        if form.is_valid():
            scheduled_days = ScheduledDay.objects.filter(owner__username__exact=request.user.username)
            date = timezone.datetime(year=int(form.cleaned_data['year']), month=int(form.cleaned_data['month']), day=int(form.cleaned_data['day']))
            selected_day = None
            start_day_date = None

            for day in scheduled_days:
                if day.date == date.date():
                    selected_day = day
                    break

            # Get date of first day in a week
            for week_day in WEEK_DAYS:
                if week_day[0] == selected_day.date.strftime('%A'):
                    start_day_date = selected_day.date - timezone.timedelta(days=week_day[1])
                    break

            got_first_day = False
            week_days = []
            week_day_names = []
            for name in WEEK_DAYS:
                week_day_names.append(name[0])
            day_counter = 0
            while not scheduled_days.filter(date__exact=start_day_date).exists():
                start_day_date += timezone.timedelta(days=1)
                week_days.append(WeekDay(week_day_names[day_counter]))
                day_counter += 1
            for day in scheduled_days:
                if day.date == start_day_date:
                    got_first_day = True
                if got_first_day:
                    week_days.append(WeekDay(week_day_names[day_counter], day))
                    day_counter += 1
                    if day_counter == 7:
                        break

            context = {
                'form': form,
                'week_days': week_days
            }

            return render(request, 'schedule_manager/scheduleweek.html', context=context)

    form = ScheduleWeekSelectForm()
    context = {'form': form}
    return render(request, 'schedule_manager/scheduleweek.html', context=context)
