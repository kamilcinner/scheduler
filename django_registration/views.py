from django.urls import reverse_lazy
from django.views import generic

from django_registration.forms import UserCreateModelForm


class UserCreateView(generic.CreateView):
    form_class = UserCreateModelForm
    template_name = 'auth/user_form.html'

    def get_success_url(self):
        return reverse_lazy('blog:user-welcome')
