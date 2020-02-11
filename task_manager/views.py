from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views import generic

from task_manager.forms import TaskCreateModelForm, TaskUpdateModelForm
from task_manager.models import Task, ShoppingList, ShoppingListItem


def index_view(request):
    return render(request, 'task_manager/index.html', context={})

def inactive_yet_view(request):
    return render(request, 'task_manager/inactive.html', context={})


class TaskListView(LoginRequiredMixin, generic.ListView):
    model = Task

    def get_queryset(self):
        return Task.objects.filter(owner__username__exact=self.request.user.username)


class TaskDetailView(LoginRequiredMixin, generic.DetailView):
    model = Task

    def get_queryset(self):
        return Task.objects.filter(owner__username__exact=self.request.user.username)


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
    form_class = TaskUpdateModelForm

    # Isn't this done by default?
    # def get_success_url(self):
    #     return reverse_lazy('task_manager:task-detail', args=[str(self.kwargs['pk'])])


class TaskDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Task
    success_url = reverse_lazy('task_manager:task-list')


class ShoppingListListView(LoginRequiredMixin, generic.ListView):
    model = ShoppingList

    def get_status_no_item_count(self):
        return ShoppingListItem.objects.filter(status__exact=False).count()

    def get_queryset(self):
        return ShoppingList.objects.filter(owner__username__exact=self.request.user.username)


class ShoppingListDetailView(LoginRequiredMixin, generic.DetailView):
    model = ShoppingList

    def get_queryset(self):
        return ShoppingList.objects.filter(owner__username__exact=self.request.user.username)


class ShoppingListCreateView(LoginRequiredMixin, generic.CreateView):
    model = ShoppingList
    fields = [
        'name'
    ]


@login_required
def mark_slist_item_bought(request, pk):
    item = get_object_or_404(ShoppingListItem, pk=pk)
    item.status = not item.status
    item.save()

    context = {
        'pk': item.s_list.pk,
        'shoppinglist': item.s_list
    }

    return render(request, 'task_manager/shoppinglist_detail.html', context=context)
