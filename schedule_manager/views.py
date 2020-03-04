from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from django.views import generic

from schedule_manager.forms import ScheduleWeekSelectForm, ActivityCreateModelForm
from schedule_manager.models import Activity
from schedule_manager.utils import WEEK_DAYS, WeekDay, WeekDayActivityTask
from schedule_manager.pollub_parser import get_pollub_subjects_list
from task_manager.models import Task


@login_required
def schedule_week_detail_view(request):
    activities = Activity.objects.filter(owner__username__exact=request.user.username)
    tasks = Task.objects.filter(owner__username__exact=request.user.username)

    context = {}

    if request.method == 'POST':
        form = ScheduleWeekSelectForm(request.POST)
        if form.is_valid():
            # Date from form, this is our selected day
            form_date = form.cleaned_data['date'] + timezone.timedelta(weeks=int(form.cleaned_data['week_shift']))
            form = ScheduleWeekSelectForm()
            form.fields['date'] = forms.DateField(initial=form_date.strftime('%Y-%m-%d'), label='Week day date')
        else:
            form_date = timezone.datetime.today().date()
    else:
        form = ScheduleWeekSelectForm()
        # Date from form, this is our selected day
        form_date = timezone.datetime.today().date()

    context['form'] = form

    if activities or tasks:
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
            week_days.append(WeekDay(date=week_monday_date + timezone.timedelta(days=i),
                                     week_day_activity_task_list=[]))

        # Add proper activities to every day in a week
        # adding is based on date and we're also checking if activity repeats every week (eg every Tuesday)
        got_at_least_one_activity_task = False
        for act in activities:
            if not act.status_active:
                continue
            for week_day in week_days:
                if act.date == week_day.date or (act.repeat_weekly and act.week_day_name == week_day.week_day_name):
                    week_day.week_day_activity_task_list.append(WeekDayActivityTask(pk=act.pk,
                                                                                    name=act.name,
                                                                                    description=act.description,
                                                                                    time=act.crispy_time))
                    got_at_least_one_activity_task = True
                    break

        for task in tasks:
            # Skip adding done tasks
            if task.status:
                continue
            for week_day in week_days:
                if task.due_date.date() == week_day.date:
                    new_week_day_activity_task = WeekDayActivityTask(pk=task.pk,
                                                                     name=task.name,
                                                                     description=task.description,
                                                                     time=task.crispy_time,
                                                                     priority=task.priority)
                    new_act_task_time = timezone.datetime.strptime(new_week_day_activity_task.time, '%H:%M').astimezone(timezone.get_default_timezone()).time()
                    # Add task in a proper order to the week day
                    i = 0
                    for act_task in week_day.week_day_activity_task_list:
                        act_task_time = timezone.datetime.strptime(act_task.time[:5], '%H:%M').astimezone(timezone.get_default_timezone()).time()
                        if new_act_task_time < act_task_time:
                            week_day.week_day_activity_task_list.insert(i, new_week_day_activity_task)
                            got_at_least_one_activity_task = True
                            break
                        i += 1
                    else:
                        week_day.week_day_activity_task_list.append(new_week_day_activity_task)
                        got_at_least_one_activity_task = True
                    break

        if got_at_least_one_activity_task:
            context['week_days'] = week_days

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


# @login_required
# def change_activity_status(request, pk):
#     activity = get_object_or_404(Activity, pk=pk)
#     if request.user.username != activity.owner.username:
#         raise Http404
#
#     activity.status_active = not activity.status_active
#     activity.save()
#
#     return HttpResponseRedirect(reverse('schedule_manager:activity-detail', args=[str(activity.pk)]))
#
#
# @login_required
# def change_repeat_status(request, pk):
#     activity = get_object_or_404(Activity, pk=pk)
#     if request.user.username != activity.owner.username:
#         raise Http404
#
#     activity.repeat_weekly = not activity.repeat_weekly
#     activity.save()
#
#     return HttpResponseRedirect(reverse('schedule_manager:activity-detail', args=[str(activity.pk)]))


@login_required
def activity_pollub_get_view(request):
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


@login_required
def activity_delete_all_view(request):
    if request.method == 'POST':
        for act in Activity.objects.filter(owner__username__exact=request.user.username):
            act.delete()

        return HttpResponseRedirect(reverse('schedule_manager:activity-list'))
    return render(request, 'schedule_manager/activity_confirm_delete_all.html', context={})


@login_required
def activity_pollub_select_view(request):
    return render(request, 'schedule_manager/activity_pollub_get.html', context={})