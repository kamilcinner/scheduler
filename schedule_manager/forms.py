from django import forms
from django.utils import timezone

from schedule_manager.models import Activity


class ScheduleWeekSelectForm(forms.Form):
    date = forms.DateField(initial=timezone.datetime.today().strftime('%Y-%m-%d'), label='Week day date')
    week_shift = forms.IntegerField(initial=0)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['week_shift'].widget = forms.HiddenInput()


class ActivityCreateModelForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = '__all__'
        exclude = ['id', 'owner']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            if field in ['status_active', 'repeat_weekly']:
                class_set = 'custom-control-input'
            else:
                class_set = 'form-control bg-scheduler-dark-3'
            self.fields[field].widget.attrs.update({'class': class_set})
