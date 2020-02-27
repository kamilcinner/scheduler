from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views import generic

from task_manager.forms import TaskCreateModelForm
from task_manager.models import Task


class TaskListView(LoginRequiredMixin, generic.ListView):
    model = Task

    def get_queryset(self):
        return Task.objects.filter(owner__username__exact=self.request.user.username)


class TaskDetailView(generic.DetailView):
    model = Task

    # def get_queryset(self):
    #     task = get_object_or_404(Task, pk=self.kwargs['pk'])
    #     if task.is_shared:
    #         return Task.objects.filter(id__exact=self.kwargs['pk'])
    #     if self.request.user.is_authenticated:
    #         return Task.objects.filter(owner__username__exact=self.request.user.username)
    #     return Task.objects.none()
    
    def get_queryset(self):
        task = get_object_or_404(Task, pk=self.kwargs['pk'])
        if task.is_shared:
            return Task.objects.filter(id__exact=self.kwargs['pk'])
        if self.request.user.is_authenticated:
            if self.request.user.username == task.owner.username:
                return Task.objects.filter(id__exact=self.kwargs['pk'])
        # Django automatically raise 404 if no object matches the query
        return Task.objects.none()


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
    form_class = TaskCreateModelForm

    def get(self, request, *args, **kwargs):
        task = get_object_or_404(Task, pk=self.kwargs['pk'])
        if task.owner.username != request.user.username:
            raise Http404
        else:
            return super().get(request, *args, **kwargs)


class TaskDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Task
    success_url = reverse_lazy('task_manager:task-list')

    def get(self, request, *args, **kwargs):
        task = get_object_or_404(Task, pk=self.kwargs['pk'])
        if task.owner.username != request.user.username:
            raise Http404
        else:
            return super().get(request, *args, **kwargs)


@login_required
def mark_task_done(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if task.owner.username != request.user.username:
        raise Http404

    task.status = not task.status
    task.save()

    return HttpResponseRedirect(reverse('task_manager:task-detail', args=[str(task.pk)]))


@login_required
def share_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if task.owner.username != request.user.username:
        raise Http404

    task.is_shared = not task.is_shared
    task.save()

    return HttpResponseRedirect(reverse('task_manager:task-detail', args=[str(task.pk)]))
