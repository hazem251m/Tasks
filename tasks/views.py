from datetime import date
import datetime
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.core.paginator import Paginator
from accounts.models import Officer
from .models import Task, TaskNotes
from .forms import TaskForm
# Create your views here.

@login_required()
def home(request):
    officer_role = request.user.officer.role
    state = request.GET.get('state')
    if officer_role == '2':
        if state:
            top_tasks = Task.objects.filter(officers__id =request.user.officer.id,state = state).order_by('-created')
        else:
            top_tasks = Task.objects.filter(officers__id =request.user.officer.id).order_by('-created')
        all_tasks = Task.objects.filter(officers__id =request.user.officer.id).count()
        completed_tasks = Task.objects.filter(officers__id =request.user.officer.id,state="تم إنجازه").count()
        pending_tasks = Task.objects.filter(officers__id =request.user.officer.id,state="بإنتظار تأكيد الإنهاء").count()
        working_on_tasks = Task.objects.filter(officers__id =request.user.officer.id,state="جاري التنفيذ").count()
        
    else: 
        if state:
            top_tasks = Task.objects.filter(state = state).order_by('-created')
        else:
            top_tasks = Task.objects.all().order_by('-created')
        all_tasks = Task.objects.all().count()
        completed_tasks = Task.objects.filter(state="تم إنجازه").count()
        pending_tasks = Task.objects.filter(state="بإنتظار تأكيد الإنهاء").count()
        working_on_tasks = Task.objects.filter(state="جاري التنفيذ").count()
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = TaskForm()
    paginator = Paginator(top_tasks, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'page_obj': page_obj, 'form': form, 'completed_tasks': completed_tasks,
               'pending_tasks': pending_tasks, 'working_on_tasks': working_on_tasks,
               'all_tasks':all_tasks}
    return render(request, 'tasks/home.html', context)

@login_required()
def add_task(request):
    today = date.today().strftime('%d/%m/%Y')
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        start_date =datetime.datetime.strptime(request.POST.get('start_date'), "%d/%m/%Y") 
        end_date = datetime.datetime.strptime(request.POST.get('end_date'), "%d/%m/%Y") 
        added_officers = request.POST.getlist('officers')
        note = request.POST.get('notes')
        attachement = request.FILES.get('attachement')
        task = Task.objects.create(title=title, description=description,
                                   start_date=start_date, end_date=end_date, task_attachment=attachement)
        officers = Officer.objects.filter(user__id__in=added_officers)
        task.save()
        task.officers.set(officers)
        task_note = TaskNotes.objects.create(task=task, note=note,officer = request.user.officer)
        task_note.save()
        return redirect('home')
    officers = Officer.objects.filter(role='2')
    context = {'officers': officers,
               'today': today,
               }
    return render(request, 'tasks/add_task.html', context=context)

@login_required()
def preview_task(request, id):
    target_task = Task.objects.get(id=id)
    all_officers = Officer.objects.filter(role='2')
    end_date = target_task.end_date
    start_date = target_task.start_date
    end_date_str = datetime.datetime.strftime(end_date, '%d/%m/%Y')
    start_date_str = datetime.datetime.strftime(start_date, '%d/%m/%Y')
    associated_officers = target_task.officers.all()
    file_name = target_task.task_attachment.name.split('/')[-1]
    context = {'target_task': target_task, 'end_date': end_date_str, 'start_date': start_date_str,
               'associated_officers': associated_officers, 'officers': all_officers, 'file_name': file_name}
    return render(request, 'tasks/edit_task.html', context)

@login_required()
def end_task(request, id):
    target_task = Task.objects.get(id=id)
    officer_role = request.user.officer.role
    if officer_role == '2' and target_task.state == 'جاري التنفيذ':
        target_task.state = 'بإنتظار تأكيد الإنهاء'
        target_task.save()    
    if officer_role == '1':
        target_task.state = 'تم إنجازه'
        target_task.save()
    return redirect('/')

@login_required()
def edit_task(request,id):
    task = Task.objects.get(id = id)
    task.title = request.POST.get('title')
    task.description = request.POST.get('description')
    task.start_date =datetime.datetime.strptime(request.POST.get('start_date'), "%d/%m/%Y") 
    task.end_date = datetime.datetime.strptime(request.POST.get('end_date'), "%d/%m/%Y") 
    added_officers=    request.POST.getlist('officers')   
    officers = Officer.objects.filter(user__id__in=added_officers)
    task.officers.set(officers)
    task.task_attachment = request.FILES.get('attachement')
    task.save()
    return redirect('/')

@login_required()
def pdf_view(request, path):
    with open(path, 'rb') as pdf:
        response = HttpResponse(pdf.read(), content_type='application/pdf')
        response['Content-Disposition'] = 'filename=some_file.pdf'
        return response

###################################################################################

@login_required()
def task_notes(request,id):
    target_task_notes = TaskNotes.objects.filter(task__id=id)
    task = Task.objects.get(id=id)
    context = {'notes':target_task_notes,'task':task}
    return render(request,'notes/task_notes.html',context=context)

@login_required()
def add_note(request,id):
    task = Task.objects.get(id=id)
    officer = Officer.objects.get(user=request.user)
    note = request.POST.get('notes')
    TaskNotes.objects.create(task=task,officer=officer,note=note)
    return task_notes(request,id)

@login_required()
def delete_task(request,id):
    task = Task.objects.get(id=id).delete()
    return redirect('/')