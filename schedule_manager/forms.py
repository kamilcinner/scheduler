from django import forms
from django.utils import timezone

from task_manager.utils import MONTH_CHOICES as MC


class ScheduleWeekSelectForm(forms.Form):
    def __init__(self, *args, **kwargs):
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
