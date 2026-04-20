from django.shortcuts import render, redirect, get_object_or_404
from .models import Task
from .forms import TaskForm


def task_list_and_create(request):

    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("crud:crud_list")

    else:
        form = TaskForm()

    # tasks = Task.objects.all()

    completed_tasks = Task.objects.filter(is_completed=True)
    incomplete_tasks = Task.objects.filter(is_completed=False)

    context = {
        "form": form,
        "completed_tasks": completed_tasks,
        "incomplete_tasks": incomplete_tasks,
    }
    return render(request, "tasklist.html", context)


def update_task(request, task_id):
    if request.method == "POST":
        task = Task.objects.get(id=task_id)
        task.is_completed = not task.is_completed
        task.save()

    return redirect("crud:crud_list")


def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    initial_data = {
        "title": task.title,
        "description": task.description,
    }

    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect("crud:crud_list")

    else:
        form = TaskForm(instance=task, initial=initial_data)

    return render(request, "edit_task.html", {"form": form, "task_id": task_id})


def delete_task(request, task_id):
    if request.method == "POST":
        task = Task.objects.get(id=task_id)
        task.delete()
        return redirect("crud:crud_list")
