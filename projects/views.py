from django.shortcuts import render, redirect, get_object_or_404
from .models import Project
from .forms import ProjectForm


def project_list(request):
    projects = Project.objects.all()

    context = {
        'projects': projects,
        'total_projects': projects.count(),
    }

    return render(request, 'projects/project_list.html', context)


def project_create(request):

    if request.method == 'POST':
        form = ProjectForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('project_list')

    else:
        form = ProjectForm()

    return render(
        request,
        'projects/project_form.html',
        {
            'form': form,
            'is_edit': False,
        }
    )


def project_detail(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    context = {
        'project': project,
    }

    return render(
        request,
        'projects/project_detail.html',
        context
    )


def project_edit(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)

        if form.is_valid():
            form.save()
            return redirect('project_detail', project_id=project.id)

    else:
        form = ProjectForm(instance=project)

    return render(
        request,
        'projects/project_form.html',
        {
            'form': form,
            'project': project,
            'is_edit': True,
        }
    )



def project_delete(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    if request.method == 'POST':
        project.delete()
        return redirect('project_list')

    return render(
        request,
        'projects/project_confirm_delete.html',
        {'project': project}
    )

