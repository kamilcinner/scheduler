from django.shortcuts import render

from shoppinglist_manager.models import ShoppingList
from task_manager.models import Task


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
    return render(request, 'index.html', context=context)


def inactive_yet_view(request):
    return render(request, 'inactive.html', context={})


def about_view(request):
    return render(request, 'about.html', context={})


def other_projects_view(request):
    return render(request, 'other_projects.html', context={})