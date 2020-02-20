from django import forms

from shoppinglist_manager.models import ShoppingList, ShoppingListItem


class ShoppingListCreateModelForm(forms.ModelForm):
    class Meta:
        model = ShoppingList
        fields = ['name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control bg-scheduler-dark-3'})


class ShoppingListItemCreateModelForm(forms.ModelForm):
    class Meta:
        model = ShoppingListItem
        fields = ['name', 'status']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control bg-scheduler-dark-3'})
        self.fields['status'].widget = forms.HiddenInput()
