from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from .models import Todo
from .forms import TodoForm
from django.http import HttpResponseRedirect
from django.db.models import Q # new

class IndexView(generic.ListView):
    template_name = 'todos/index.html'
    context_object_name = 'todo_list'

    def get_queryset(self):
        query = self.request.GET.get("q")
        if query != None:
                object_list = Todo.objects.filter(
                    Q(title__icontains=query) | Q(title__icontains=query)
                    )
                return object_list
        else:
            return Todo.objects.order_by('-created_at')
        

def add(request):
    if request.method == 'POST':
        form = TodoForm(request.POST)

        if form.is_valid():
            form.save()

    # title = request.POST[['title'], ['description'], ['due']]
    # Todo.objects.create(title=title, description=description, )

    return redirect('todos:index')

def delete(request, todo_id):
    todo = get_object_or_404(Todo, pk=todo_id)
    todo.delete()

    return redirect('todos:index')

def complete(request, todo_id):
    todo = get_object_or_404(Todo, pk=todo_id)
    isCompleted = request.POST.get('isCompleted', False)
    if isCompleted == 'on':
        isCompleted = True
    
    todo.isCompleted = isCompleted

    todo.save()
    return redirect('todos:index')


def update(request, todo_id):
    task = Todo.objects.get(pk=todo_id)

    form = TodoForm(instance=task)

    if request.method == 'POST':
        form = TodoForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
        return redirect('/')

    context = {'form': form}

    return render(request, 'todos/update.html', context)


