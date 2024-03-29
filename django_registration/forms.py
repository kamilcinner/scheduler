from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.mail import EmailMessage

from scheduler import settings


class UserCreateModelForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'username',
            'email'
        ]
        help_texts = {
            'username': 'Min 8 and max 20 characters, allowing: letters, digits and {@.+-_}.'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control bg-scheduler-dark-3'})

    # password1 = forms.PasswordInput() - doesn't work properly
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    def clean_username(self):
        # Check that the username len <= 20 and len >= 8
        username = self.cleaned_data.get('username')
        if len(username) > 20:
            raise forms.ValidationError('Username too long.')
        elif len(username) < 8:
            raise forms.ValidationError('Username too short.')
        return username

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match.")
        # Use django built in password validation
        validate_password(password2)
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            self.send_registration_confirmation_email()
            user.save()
        return user

    def send_registration_confirmation_email(self):
        email = EmailMessage(
            'Thank You for registration!',
            'We are willing to spend some awesome time together :)',
            settings.EMAIL_HOST_USER,
            [self.cleaned_data.get('email')]
        )
        email.send(fail_silently=True)
