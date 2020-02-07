from django.shortcuts import render


def index_view(request):
    return render(request, 'task_manager/index.html', context={})