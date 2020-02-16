from django import forms
from django.utils import timezone

from task_manager.models import Task, ShoppingList, ShoppingListItem


class TaskCreateModelForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = [
            'name',
            'description',
            'priority'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.generate_year_choices()
        self.fields['year'] = forms.ChoiceField(choices=self.YEAR_CHOICES)
        self.generate_day_choices()
        self.fields['day'] = forms.ChoiceField(choices=self.DAY_CHOICES)
        self.generate_hour_choices()
        self.fields['hour'] = forms.ChoiceField(choices=self.HOUR_CHOICES)
        self.generate_minute_choices()
        self.fields['minute'] = forms.ChoiceField(choices=self.MINUTE_CHOICES)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control bg-scheduler-dark-2'})
        self.set_initial_due_date()

    def set_initial_due_date(self):
        date = self.instance.due_date.astimezone(timezone.get_default_timezone())

        self.fields['year'].initial = date.year
        self.fields['month'].initial = date.month
        self.fields['day'].initial = date.day
        self.fields['hour'].initial = date.hour
        self.fields['minute'].initial = date.minute

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

    def generate_hour_choices(self):
        for hour in range(0, 24):
            if hour < 10:
                content = f'0{hour}'
            else:
                content = str(hour)
            self.HOUR_CHOICES += (tuple((hour, content)),)

    def generate_minute_choices(self):
        for minute in range(0, 60):
            if minute < 10:
                content = f'0{minute}'
            else:
                content = str(minute)
            self.MINUTE_CHOICES += (tuple((minute, content)),)

    YEAR_CHOICES = ()
    year = forms.ChoiceField(choices=YEAR_CHOICES)

    MONTH_CHOICES = (
        (1, 'january'),
        (2, 'february'),
        (3, 'march'),
        (4, 'april'),
        (5, 'may'),
        (6, 'august'),
        (7, 'june'),
        (8, 'july'),
        (9, 'september'),
        (10, 'october'),
        (11, 'november'),
        (12, 'december')
    )

    month = forms.ChoiceField(choices=MONTH_CHOICES)
    DAY_CHOICES = ()
    day = forms.IntegerField(min_value=1)
    HOUR_CHOICES = ()
    hour = forms.ChoiceField(choices=HOUR_CHOICES)
    MINUTE_CHOICES = ()
    minute = forms.ChoiceField(choices=MINUTE_CHOICES)

    def is_leap_year(self, year):
        if year % 4 == 0:
            if year % 100 == 0:
                if year % 400 == 0:
                    return  True
            else:
                return True
        return False

    def clean_day(self):
        year = int(self.cleaned_data['year'])
        month = int(self.cleaned_data['month'])
        day = int(self.cleaned_data['day'])
        lesser_months = {2, 4, 6, 9, 11}
        month_str = self.MONTH_CHOICES[month - 1][1].capitalize()

        if day > 28 and month == 2 and not self.is_leap_year(year):
            raise forms.ValidationError(f"{month_str} has only 28 days because entered year is not a leap year.")
        elif day > 29 and month == 2:
            raise forms.ValidationError(f"{month_str} has only 29 days despite of entered year is a leap year.")
        elif day > 30 and month in lesser_months:
            raise forms.ValidationError(f"{month_str} has only 30 days.")
        elif day > 31:
            raise forms.ValidationError(f"{month_str} has only 31 days.")

        return day

    def save(self, commit=True):
        year = int(self.cleaned_data['year'])
        month = int(self.cleaned_data['month'])
        day = int(self.cleaned_data['day'])
        hour = int(self.cleaned_data['hour'])
        minute = int(self.cleaned_data['minute'])

        task = super().save(commit=False)
        task.due_date = timezone.datetime(year=year, month=month, day=day, hour=hour, minute=minute)

        if commit:
            task.save()
        return task


class ShoppingListCreateModelForm(forms.ModelForm):
    class Meta:
        model = ShoppingList
        fields = ['name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control bg-scheduler-dark-2'})


class ShoppingListItemCreateModelForm(forms.ModelForm):
    class Meta:
        model = ShoppingListItem
        fields = ['name', 'status']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control bg-scheduler-dark-3'})
        self.fields['status'].widget = forms.HiddenInput()
