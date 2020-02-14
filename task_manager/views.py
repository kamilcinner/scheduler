from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import formset_factory
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.views import generic

from task_manager.forms import TaskCreateModelForm, ShoppingListCreateModelForm, \
    ShoppingListItemCreateModelForm
from task_manager.models import Task, ShoppingList, ShoppingListItem


def index_view(request):
    if request.user.is_authenticated:
        num_tasks = Task.objects.filter(owner__username__exact=request.user.username, status__exact=False).count()
        num_active_slist = 0
        for slist in ShoppingList.objects.filter(owner__username__exact=request.user.username):
            for item in slist.shoppinglistitem_set.all():
                if not item.status:
                    num_active_slist += 1
                    break
        context = {
            'num_tasks': num_tasks,
            'num_active_slist': num_active_slist
        }
    else:
        context = {}
    return render(request, 'task_manager/index.html', context=context)


def inactive_yet_view(request):
    return render(request, 'task_manager/inactive.html', context={})


def about_view(request):
    return render(request, 'task_manager/about.html', context={})


def other_projects_view(request):
    return render(request, 'task_manager/other_projects.html', context={})


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
    form_class = TaskCreateModelForm

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


class ShoppingListDetailView(generic.DetailView):
    model = ShoppingList

    def get_queryset(self):
        slist = get_object_or_404(ShoppingList, pk=self.kwargs['pk'])
        if slist.is_shared:
            return ShoppingList.objects.filter(id__exact=self.kwargs['pk'])
        if self.request.user.is_authenticated:
            return ShoppingList.objects.filter(owner__username__exact=self.request.user.username)
        return ShoppingList.objects.none()


class ShoppingListCreateView(LoginRequiredMixin, generic.CreateView):
    model = ShoppingList
    form_class = ShoppingListCreateModelForm

    def get_success_url(self):
        return reverse_lazy('task_manager:slist-update', args=[str(self.object.id)])

    def form_valid(self, form):
        """
        Add user to form data before setting it as valid (so it is saved to model)
        """
        form.instance.owner = self.request.user
        form.instance.date_added = timezone.now()
        return super().form_valid(form)


@login_required
def shoppinglist_update_view(request, pk):
    s_list = get_object_or_404(ShoppingList, pk=pk)
    ShoppingListItemFormSet = formset_factory(ShoppingListItemCreateModelForm, extra=1, max_num=50, validate_max=True)
    if request.method == 'POST':
        formset = ShoppingListItemFormSet(request.POST)
        if formset.is_valid():
            for item in s_list.shoppinglistitem_set.all():
                item.delete()
            for form in formset:
                if not form.has_changed():
                    continue
                if form.cleaned_data['name'] == '':
                    continue
                item = ShoppingListItem()
                item.s_list = s_list
                item.name = form.cleaned_data['name']
                item.status = form.cleaned_data['status']
                item.save()
            return HttpResponseRedirect(reverse('task_manager:slist-detail', args=[str(pk)]))
    else:
        initial_data = []
        for item in s_list.shoppinglistitem_set.all():
            initial_data.append({'name': item.name, 'status': item.status})
        formset = ShoppingListItemFormSet(initial=initial_data)

    context = {
        'shoppinglist': s_list,
        'formset': formset
    }
    return render(request, 'task_manager/shoppinglist_update.html', context)


class ShoppingListDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = ShoppingList
    success_url = reverse_lazy('task_manager:slist-list')

    def delete(self, request, *args, **kwargs):
        obj = get_object_or_404(self.model, pk=kwargs['pk'])
        for item in obj.shoppinglistitem_set.all():
            item.delete()
        return super().delete(request, *args, **kwargs)


# @login_required
def mark_slist_item_bought(request, pk):
    item = get_object_or_404(ShoppingListItem, pk=pk)
    if not item.s_list.is_shared and item.s_list.owner.username != request.user.username:
        raise Http404
    else:
        item.status = not item.status
        item.save()
        return HttpResponseRedirect(reverse('task_manager:slist-detail', args=[str(item.s_list.pk)]))


@login_required
def mark_task_done(request, pk):
    task = get_object_or_404(Task, pk=pk)
    task.status = not task.status
    task.save()

    return HttpResponseRedirect(reverse('task_manager:task-detail', args=[str(task.pk)]))


@login_required
def share_slist(request, pk):
    slist = get_object_or_404(ShoppingList, pk=pk)
    slist.is_shared = not slist.is_shared
    slist.save()

    return HttpResponseRedirect(reverse('task_manager:slist-detail', args=[str(slist.pk)]))
