from django import forms
from django.utils import timezone

from schedule_manager.models import Activity#, ScheduledDay
from task_manager.utils import MONTH_CHOICES as MC


# TODO: add custom validation for fields where needed
class ScheduleWeekSelectForm(forms.Form):
    def __init__(self, *args, **kwargs):
        # self.request = kwargs.pop('request')  # TODO: check if this work
        super().__init__(*args, **kwargs)
        self.generate_year_choices()
        self.fields['year'] = forms.ChoiceField(choices=self.YEAR_CHOICES)
        self.generate_day_choices()
        self.fields['day'] = forms.ChoiceField(choices=self.DAY_CHOICES)

        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control bg-scheduler-dark-3'})

        self.set_initial_date()

    def set_initial_date(self):
        date = timezone.datetime.today()

        self.fields['year'].initial = date.year
        self.fields['month'].initial = date.month
        self.fields['day'].initial = date.day

    def generate_year_choices(self):
        current_year = timezone.datetime.today().year
        for year in range(current_year, current_year + 20):
            self.YEAR_CHOICES += (tuple((year, str(year))),)

    def generate_day_choices(self):
        for day in range(1, 32):
            if day < 10:
                content = f'0{day}'
            else:
                content = str(day)
            self.DAY_CHOICES += (tuple((day, content)),)

    YEAR_CHOICES = ()
    MONTH_CHOICES = MC
    DAY_CHOICES = ()

    year = forms.ChoiceField(choices=YEAR_CHOICES)
    month = forms.ChoiceField(choices=MONTH_CHOICES)
    day = forms.ChoiceField(choices=DAY_CHOICES)


class ActivityCreateModelForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = [
            'name',
            'time_start',
            'time_end',
            'date',
            'status_active',
            'repeat_weekly'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control bg-scheduler-dark-3'})

    # def set_initial_due_date(self):
    #     date = self.instance.due_date.astimezone(timezone.get_default_timezone())
    #
    #     self.fields['year'].initial = date.year
    #     self.fields['month'].initial = date.month
    #     self.fields['day'].initial = date.day
    #     self.fields['hour'].initial = date.hour
    #     self.fields['minute'].initial = date.minute

    date = forms.DateField(initial=timezone.datetime.today(), label='Scheduled Day date')


    # def save(self, commit=True):
    #     activity = super().save(commit=False)
    #
    #
    #
    #
    #     if commit:
    #         activity.save()
    #     return activity