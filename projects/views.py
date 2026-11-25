from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q, Prefetch
from .models import Project
from .forms import ProjectForm
from django.core.paginator import Paginator
from performance.models import DataEntry



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

    metrics = project.metrics.prefetch_related(
        Prefetch(
            'entries',
            queryset=DataEntry.objects.order_by(
                '-recorded_at',
                '-created_at'
            ),
            to_attr='measurement_entries'
        )
    )

    metric_status_counts = {
        'On Target': 0,
        'Off Target': 0,
        'Awaiting Data': 0,
        'No Target': 0,
    }

    total_metrics = metrics.count()

    for metric in metrics:

        latest_entry = (
            metric.measurement_entries[0]
            if metric.measurement_entries
            else None
        )

        performance_status = 'Awaiting Data'

        if latest_entry:

            if metric.target_value is None:

                performance_status = 'No Target'

            elif metric.direction == 'Decrease':

                if latest_entry.value <= metric.target_value:
                    performance_status = 'On Target'
                else:
                    performance_status = 'Off Target'

            elif metric.direction == 'Increase':

                if latest_entry.value >= metric.target_value:
                    performance_status = 'On Target'
                else:
                    performance_status = 'Off Target'

            elif metric.direction == 'Maintain':

                if latest_entry.value == metric.target_value:
                    performance_status = 'On Target'
                else:
                    performance_status = 'Off Target'

        metric.performance_status = performance_status

        metric_status_counts[performance_status] += 1

    on_target_percentage = (
        round(
            (metric_status_counts['On Target'] / total_metrics) * 100,
            1
        )
        if total_metrics > 0
        else 0
    )

    phases = project.dmaic_phases.all()

    total_phases = phases.count()

    completed_phases = phases.filter(
        status='Completed'
    ).count()

    progress_percentage = (
        (completed_phases / total_phases) * 100
        if total_phases > 0
        else 0
    )

    context = {
        'project': project,
        'total_phases': total_phases,
        'completed_phases': completed_phases,
        'progress_percentage': progress_percentage,
        'metrics': metrics,
        'metric_status_counts': metric_status_counts,
        'on_target_count': metric_status_counts['On Target'],
        'off_target_count': metric_status_counts['Off Target'],
        'awaiting_data_count': metric_status_counts['Awaiting Data'],
        'no_target_count': metric_status_counts['No Target'],
        'total_metrics': total_metrics,
        'on_target_percentage': on_target_percentage,
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

