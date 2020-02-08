from django.contrib.auth.models import User
from django.forms import ModelForm, forms
from django import forms

from django.contrib.auth.password_validation import validate_password


class UserCreateModelForm(ModelForm):
    class Meta:
        model = User
        fields = [
            'username'
        ]
        help_texts = {
            'username': 'Min 8 and max 20 characters, allowing: letters, digits and {@.+-_}.'
        }

    # password1 = forms.PasswordInput() - doesn't work properly
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match.")
        # Use django built in password validation
        validate_password(password2)

        return password2

    def clean_username(self):
        # Check that the username len <= 20 and len >= 8
        username = self.cleaned_data.get('username')
        if 8 > len(username) > 20:
            raise forms.ValidationError('Username too long.')

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
