from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from .models import Project
from .forms import ProjectForm
from django.core.paginator import Paginator




def project_list(request):

    projects = Project.objects.all()

    search_query = request.GET.get('q', '')
    selected_status = request.GET.get('status', '')
    selected_priority = request.GET.get('priority', '')

    # Search
    if search_query:
        projects = projects.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query)
        )

    # Status Filter
    if selected_status:
        projects = projects.filter(status=selected_status)

    # Priority Filter
    if selected_priority:
        projects = projects.filter(priority=selected_priority)

    # Pagination
    paginator = Paginator(projects, 10)
    page_number = request.GET.get('page')
    projects_page = paginator.get_page(page_number)

    # Preserve active filters when changing pages
    filter_query = request.GET.copy()
    filter_query.pop('page', None)
    filter_query = filter_query.urlencode()

    active_projects = Project.objects.filter(
        status='In Progress'
    ).count()

    completed_projects = Project.objects.filter(
        status='Completed'
    ).count()

    on_hold_projects = Project.objects.filter(
        status='On Hold'
    ).count()

    context = {
        'projects': projects_page,
        'total_projects': Project.objects.count(),
        'search_query': search_query,
        'selected_status': selected_status,
        'selected_priority': selected_priority,
        'filter_query': filter_query,

        'active_projects': active_projects,
        'completed_projects': completed_projects,
        'on_hold_projects': on_hold_projects,
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

