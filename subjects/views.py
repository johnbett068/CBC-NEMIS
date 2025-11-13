from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Subject

@login_required
def subject_list(request):
    subjects = Subject.objects.all().order_by('name')
    return render(request, 'subjects/subject_list.html', {'subjects': subjects})

@login_required
def subject_add(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        code = request.POST.get('code')
        Subject.objects.create(name=name, code=code)
        messages.success(request, "Subject added successfully.")
        return redirect('subjects:subject_list')
    return render(request, 'subjects/subject_add.html')
