from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import formset_factory
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.views import generic

from shoppinglist_manager.forms import ShoppingListCreateModelForm, ShoppingListItemCreateModelForm
from shoppinglist_manager.models import ShoppingList, ShoppingListItem


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
        return reverse_lazy('shoppinglist_manager:slist-update', args=[str(self.object.id)])

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
    if s_list.owner.username != request.user.username:
        raise Http404
    ShoppingListItemFormSet = formset_factory(ShoppingListItemCreateModelForm, extra=1, max_num=50, validate_max=True)
    if request.method == 'POST':
        formset = ShoppingListItemFormSet(request.POST)
        if formset.is_valid():
            # Updating list last edit
            s_list.date_added = timezone.now()
            s_list.save()

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
            return HttpResponseRedirect(reverse('shoppinglist_manager:slist-detail', args=[str(pk)]))
    else:
        initial_data = []
        for item in s_list.shoppinglistitem_set.all():
            initial_data.append({'name': item.name, 'status': item.status})
        formset = ShoppingListItemFormSet(initial=initial_data)

    context = {
        'shoppinglist': s_list,
        'formset': formset
    }
    return render(request, 'shoppinglist_manager/shoppinglist_update.html', context)


class ShoppingListDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = ShoppingList
    success_url = reverse_lazy('shoppinglist_manager:slist-list')

    def get(self, request, *args, **kwargs):
        slist = get_object_or_404(ShoppingList, pk=self.kwargs['pk'])
        if slist.owner.username != request.user.username:
            raise Http404
        else:
            return super().get(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        obj = get_object_or_404(self.model, pk=kwargs['pk'])
        for item in obj.shoppinglistitem_set.all():
            item.delete()
        return super().delete(request, *args, **kwargs)


def mark_slist_item_bought(request, pk):
    item = get_object_or_404(ShoppingListItem, pk=pk)
    if not item.s_list.is_shared and item.s_list.owner.username != request.user.username:
        raise Http404
    else:
        item.status = not item.status
        item.save()
        return HttpResponseRedirect(reverse('shoppinglist_manager:slist-detail', args=[str(item.s_list.pk)]))


@login_required
def share_slist(request, pk):
    slist = get_object_or_404(ShoppingList, pk=pk)
    if slist.owner.username != request.user.username:
        raise Http404

    slist.is_shared = not slist.is_shared
    slist.save()

    return HttpResponseRedirect(reverse('shoppinglist_manager:slist-detail', args=[str(slist.pk)]))
