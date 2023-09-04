# from django.shortcuts import render
# from .models import Task



from django.shortcuts import render, redirect, get_object_or_404
from .models import Task
from .forms import TaskForm
import json
from django.http import JsonResponse

def kanban_board(request):
    todo_tasks = Task.objects.filter(status='To Do')
    in_progress_tasks = Task.objects.filter(status='In Progress')
    done_tasks = Task.objects.filter(status='Done')
    
    return render(request, 'kanban_board.html', {
        'todo_tasks': todo_tasks,
        'in_progress_tasks': in_progress_tasks,
        'done_tasks': done_tasks,
    })

def add_task_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        title = data.get('title')
        status = data.get('status', 'To Do')  # Default to "To Do" if status is not provided

        if title:
            task = Task.objects.create(title=title, status=status)
            return JsonResponse({'success': True})
    return JsonResponse({'success': False})

def update_task_status(request, task_id):
    try:
        # Retrieve the task based on task_id
        task = Task.objects.get(id=task_id)

        data = json.loads(request.body)
        new_status = data.get('newStatus', None)  # Retrieve the new status

        if new_status is not None:
            print(new_status)
            task.status = new_status
            task.save()

        return JsonResponse({'message': 'Task status updated successfully'})

    except Task.DoesNotExist:
        return JsonResponse({'error': 'Task not found'}, status=404)
    
    except Exception as e:
        # Handle other exceptions and log the error for debugging
        print(str(e))
        return JsonResponse({'error': 'Internal Server Error'}, status=500)

def edit_task_view(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('kanban_board')
    else:
        form = TaskForm(instance=task)
    
    return render(request, 'edit_task.html', {'form': form, 'task': task})

def delete_task_view(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.delete()
    return redirect('kanban_board')
