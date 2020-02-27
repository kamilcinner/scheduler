from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from django.views import generic

from schedule_manager.forms import ScheduleWeekSelectForm, ActivityCreateModelForm
from schedule_manager.models import Activity
from schedule_manager.utils import *


@login_required
def schedule_week_detail_view(request):
    if request.method == 'POST':
        form = ScheduleWeekSelectForm(request.POST)
        activities = Activity.objects.filter(owner__username__exact=request.user.username)

        if form.is_valid() and activities:
            # List of Days with activity set
            days = []
            # Date of activities happening in ONE day
            day_activities_date = activities[0].date
            # Create first date based on activities
            current_day_activities = []

            # Create list of Days with activity set
            for act in activities:
                if act.date != day_activities_date:
                    days.append(Day(name=day_activities_date.strftime('%A'),
                                    date=day_activities_date,
                                    activities=current_day_activities))
                    current_day_activities = []

                    day_activities_date = act.date

                elif act == activities.last():
                    days.append(Day(name=day_activities_date.strftime('%A'),
                                    date=day_activities_date,
                                    activities=current_day_activities))

                current_day_activities.append(act)

            # Date from form
            date = form.cleaned_data['date']
            # Date of Monday in a week in which selected day occurs
            week_monday_date = None

            # Get date of Monday in a week in which selected day occurs
            # week_day[0] is week day name
            # week_day[1] is week day index - Monday is 0, Sunday is 6
            for week_day in WEEK_DAYS:
                if week_day[0] == date.strftime('%A'):
                    week_monday_date = date - timezone.timedelta(days=week_day[1])
                    break

            # List of Days which occurs in selected week
            week_days = []
            
            # List of week day names
            week_day_names = []
            for name in WEEK_DAYS:
                week_day_names.append(name[0])

            # Add Days to our week day list
            date = week_monday_date
            got_at_least_one_activity = False
            for i in range(0, 7):
                day = get_day_by_date(days=days, date=date)
                if day:
                    # Add Day from our list which occurs in selected week
                    week_days.append(day)
                    got_at_least_one_activity = True
                else:
                    # Add Day with no activities for proper work of our template
                    week_days.append(Day(name=week_day_names[i], date=date))
                date += timezone.timedelta(days=1)

            context = {'form': form}

            if got_at_least_one_activity:
                context['week_days'] = week_days

            return render(request, 'schedule_manager/scheduleweek.html', context=context)

    form = ScheduleWeekSelectForm()
    context = {'form': form, 'first_select': True}
    return render(request, 'schedule_manager/scheduleweek.html', context=context)


class ActivityCreateView(LoginRequiredMixin, generic.CreateView):
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


class ActivityUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Activity
    form_class = ActivityCreateModelForm
    

class ActivityDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Activity
    success_url = reverse_lazy('schedule_manager:schedule-week')
    
    
class ActivityDetailView(LoginRequiredMixin, generic.DetailView):
    model = Activity
    
    def get_queryset(self):
        activity = get_object_or_404(Activity, pk=self.kwargs['pk'])
        if self.request.user.username == activity.owner.username:
            return Activity.objects.filter(id__exact=self.kwargs['pk'])
        return Activity.objects.none()
