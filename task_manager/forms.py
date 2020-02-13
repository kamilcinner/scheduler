import datetime

from django import forms

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
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control bg-scheduler-dark'})
        self.set_initial_due_date()

    def set_initial_due_date(self):
        self.fields['year'].initial = self.instance.due_date.year
        self.fields['month'].initial = self.instance.due_date.month
        self.fields['day'].initial = self.instance.due_date.day
        self.fields['hour'].initial = self.instance.due_date.hour + 1 #TODO: fix timezone
        self.fields['minute'].initial = self.instance.due_date.minute

    year = forms.IntegerField(min_value=datetime.date.today().year)

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
    day = forms.IntegerField(min_value=1)

    HOUR_CHOICES = (
        (0, '00'),
        (1, '01'),
        (2, '02'),
        (3, '03'),
        (4, '04'),
        (5, '05'),
        (6, '06'),
        (7, '07'),
        (8, '08'),
        (9, '09'),
        (10, '10'),
        (11, '11'),
        (12, '12'),
        (13, '13'),
        (14, '14'),
        (15, '15'),
        (16, '16'),
        (17, '17'),
        (18, '18'),
        (19, '19'),
        (20, '20'),
        (21, '21'),
        (22, '22'),
        (23, '23'),
    )

    hour = forms.ChoiceField(choices=HOUR_CHOICES)

    MINUTE_CHOICES = (
        (0, '00'),
        (1, '01'),
        (2, '02'),
        (3, '03'),
        (4, '04'),
        (5, '05'),
        (6, '06'),
        (7, '07'),
        (8, '08'),
        (9, '09'),
        (10, '10'),
        (11, '11'),
        (12, '12'),
        (13, '13'),
        (14, '14'),
        (15, '15'),
        (16, '16'),
        (17, '17'),
        (18, '18'),
        (19, '19'),
        (20, '20'),
        (21, '21'),
        (22, '22'),
        (23, '23'),
        (24, '24'),
        (25, '25'),
        (26, '26'),
        (27, '27'),
        (28, '28'),
        (29, '29'),
        (30, '30'),
        (31, '31'),
        (32, '32'),
        (33, '33'),
        (34, '34'),
        (35, '35'),
        (36, '36'),
        (37, '37'),
        (38, '38'),
        (39, '39'),
        (40, '40'),
        (41, '41'),
        (42, '42'),
        (43, '43'),
        (44, '44'),
        (45, '45'),
        (46, '46'),
        (47, '47'),
        (48, '48'),
        (49, '49'),
        (50, '50'),
        (51, '51'),
        (52, '52'),
        (53, '53'),
        (54, '54'),
        (55, '55'),
        (56, '56'),
        (57, '57'),
        (58, '58'),
        (59, '59'),
    )

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
        year = self.cleaned_data['year']
        month = int(self.cleaned_data['month'])
        day = self.cleaned_data['day']
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
        year = self.cleaned_data['year']
        month = int(self.cleaned_data['month'])
        day = self.cleaned_data['day']
        hour = int(self.cleaned_data['hour'])
        minute = int(self.cleaned_data['minute'])

        task = super().save(commit=False)
        task.due_date = datetime.datetime(year=year, month=month, day=day, hour=hour, minute=minute)

        if commit:
            task.save()
        return task


# class TaskUpdateModelForm(forms.ModelForm):
#     class Meta:
#         model = Task
#         fields = '__all__'
#         exclude = ['owner']
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         for field in self.fields:
#             self.fields[field].widget.attrs.update({'class': 'form-control bg-scheduler-dark'})


class ShoppingListCreateModelForm(forms.ModelForm):
    class Meta:
        model = ShoppingList
        fields = ['name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control bg-scheduler-dark'})


class ShoppingListItemCreateModelForm(forms.ModelForm):
    class Meta:
        model = ShoppingListItem
        fields = ['name', 'status']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control bg-scheduler-dark'})
        self.fields['status'].widget = forms.HiddenInput()
