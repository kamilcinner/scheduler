from django.urls import reverse_lazy
from django.views import generic

from django_registration.forms import UserCreateForm


class UserCreateView(generic.CreateView):
    form_class = UserCreateForm
    template_name = 'auth/user_form.html'

    def get_success_url(self):
        return reverse_lazy('blog:user-welcome')
