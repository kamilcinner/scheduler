from django import forms
from django.utils import timezone

from schedule_manager.models import Activity


class ScheduleWeekSelectForm(forms.Form):
    date = forms.DateField(initial=timezone.datetime.today().strftime('%Y-%m-%d'))


class ActivityCreateModelForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = '__all__'
        exclude = ['id', 'owner']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control bg-scheduler-dark-3'})
