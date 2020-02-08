from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from task_manager.forms import TaskCreateModelForm
from task_manager.models import Task

@login_required
def index_view(request):
    return render(request, 'task_manager/index.html', context={})


class TaskListView(LoginRequiredMixin, generic.ListView):
    model = Task


class TaskDetailView(LoginRequiredMixin, generic.DetailView):
    model = Task


class TaskCreateView(LoginRequiredMixin, generic.CreateView):
    model = Task
    form_class = TaskCreateModelForm

    def form_valid(self, form):
        """
        Add user to form data before setting it as valid (so it is saved to model)
        """
        form.instance.owner = self.request.user
        return super().form_valid(form)


class TaskUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Task
    fields = '__all__'

    # Isn't this done by default?
    # def get_success_url(self):
    #     return reverse_lazy('task_manager:task-detail', args=[str(self.kwargs['pk'])])


class TaskDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Task
    success_url = reverse_lazy('task_manager:task-list')