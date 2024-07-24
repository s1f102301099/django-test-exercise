from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from django.utils.timezone import make_aware
from django.utils.dateparse import parse_datetime
from .models import Task, Comment
from .forms import CommentForm

# Create your views here.


def index(request):
    if request.method == "POST":
        task = Task(title=request.POST["title"],
                    due_at=make_aware(parse_datetime(request.POST["due_at"])))
        task.save()

    if request.GET.get("order") == "due":
        tasks = Task.objects.order_by("due_at")
    else:
        tasks = Task.objects.order_by("-posted_at")

    context = {
        "tasks": tasks
    }
    return render(request, "todo/index.html", context)

def detail(request, task_id):
    try:
        task = Task.objects.get(pk=task_id)
    except Task.DoesNotExist:
        raise Http404("Task does not exist")
    
    context = {
        'task': task,
    } 
    return render(request, 'todo/detail.html', context)


def update (request, task_id):
    try:
        task = Task.objects.get(pk=task_id)
    except Task.DoesNotExist:
        raise Http404 ("Task does not exist")
    if request.method == 'POST':
        task.title = request.POST['title']
        task.due_at = make_aware (parse_datetime(request.POST['due_at']))
        task.save()
        return redirect (detail, task_id)
        
    context = {
        'task': task
    }
    return render (request, "todo/edit.html", context)

def delete(request, task_id):
    try:
        task = Task.objects.get(pk=task_id)
    except Task.DoesNotExist:
        raise Http404("Task does not exist")
    task.delete()
    return redirect(index)

def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk)
    comments = task.comments.all()
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.task = task
            comment.author = request.user
            comment.save()
            return redirect('task_detail', pk=task.pk)
    else:
        form = CommentForm()
    return render(request, 'todo/task_detail.html', {'task': task, 'comments': comments, 'form': form})
