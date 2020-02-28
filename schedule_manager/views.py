from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from django.views import generic

from schedule_manager.forms import ScheduleWeekSelectForm, ActivityCreateModelForm
from schedule_manager.models import Activity
from schedule_manager.utils import WEEK_DAYS, WeekDay, get_pollub_subjects_list


@login_required
def schedule_week_detail_view(request):
    activities = Activity.objects.filter(owner__username__exact=request.user.username)
    if request.method == 'POST':
        form = ScheduleWeekSelectForm(request.POST)
        context = {}

        if form.is_valid() and activities:
            # Date from form, this is our selected day
            form_date = form.cleaned_data['date']

            # Get date of Monday in a week in which selected day occurs
            # week_day[0] is week day name
            # week_day[1] is week day index - Monday is 0, Sunday is 6
            week_monday_date = None
            for week_day in WEEK_DAYS:
                if week_day[0] == form_date.strftime('%A'):
                    week_monday_date = form_date - timezone.timedelta(days=week_day[1])
                    break

            # Create list of days which occurs in a week in which selected day is present
            week_days = []
            for i in range(0, 7):
                week_days.append(WeekDay(date=week_monday_date + timezone.timedelta(days=i), activities=[]))

            # Add proper activities to every day in a week
            # adding is based on date and we're also checking if activity repeats every week (eg every Tuesday)
            got_at_least_one_activity = False
            for act in activities:
                if not act.status_active:
                    continue
                for week_day in week_days:
                    if act.date == week_day.date or (act.repeat_weekly and act.get_week_day_name == week_day.get_week_day_name):
                        week_day.activities.append(act)
                        got_at_least_one_activity = True

            if got_at_least_one_activity:
                context['week_days'] = week_days

        context['form'] = form
    # If request GET
    else:
        form = ScheduleWeekSelectForm()
        context = {'form': form}

        if activities:
            context['first_select'] = True
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


class ActivityUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Activity
    form_class = ActivityCreateModelForm
    

class ActivityDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Activity
    success_url = reverse_lazy('schedule_manager:activity-list')
    
    
class ActivityDetailView(LoginRequiredMixin, generic.DetailView):
    model = Activity
    
    def get_queryset(self):
        activity = get_object_or_404(Activity, pk=self.kwargs['pk'])
        if self.request.user.username == activity.owner.username:
            return Activity.objects.filter(id__exact=self.kwargs['pk'])
        return Activity.objects.none()


class ActivityListView(LoginRequiredMixin, generic.ListView):
    model = Activity

    def get_queryset(self):
        return Activity.objects.filter(owner__username__exact=self.request.user.username)


@login_required
def change_activity_status(request, pk):
    activity = get_object_or_404(Activity, pk=pk)
    if request.user.username != activity.owner.username:
        raise Http404

    activity.status_active = not activity.status_active
    activity.save()

    return HttpResponseRedirect(reverse('schedule_manager:activity-detail', args=[str(activity.pk)]))


@login_required
def change_repeat_status(request, pk):
    activity = get_object_or_404(Activity, pk=pk)
    if request.user.username != activity.owner.username:
        raise Http404

    activity.repeat_weekly = not activity.repeat_weekly
    activity.save()

    return HttpResponseRedirect(reverse('schedule_manager:activity-detail', args=[str(activity.pk)]))


@login_required
def get_activities_from_pollub(request):
    subjects = get_pollub_subjects_list()
    for sub in subjects:
        new_activity = Activity()
        new_activity.name = sub.name
        new_activity.description = f'{sub.lecturer}, {sub.class_}'
        new_activity.status_active = False
        new_activity.repeat_weekly = True
        new_activity.time_start = timezone.datetime.strptime(sub.time_start, '%H:%M').time()
        new_activity.time_end = timezone.datetime.strptime(sub.time_end, '%H:%M').time()
        new_activity.owner = request.user
        new_activity.save()

    return HttpResponseRedirect(reverse('schedule_manager:activity-list'))


@login_required
def delete_all_user_activities(request):
    for act in Activity.objects.filter(owner__username__exact=request.user.username):
        act.delete()

    return HttpResponseRedirect(reverse('schedule_manager:activity-list'))
