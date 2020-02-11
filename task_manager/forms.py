from django import forms

from task_manager.models import Task, ShoppingList, ShoppingListItem


class TaskCreateModelForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = [
            'name',
            'due_date',
            'description',
            'priority'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control bg-scheduler-dark'})


class TaskUpdateModelForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = '__all__'
        exclude = ['owner']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control bg-scheduler-dark'})


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
