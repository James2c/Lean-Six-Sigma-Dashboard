from django.shortcuts import get_object_or_404, render, redirect

from .models import Metric, DataEntry
from .forms import DataEntryForm, MetricForm


def metric_detail(request, metric_id):

    metric = get_object_or_404(
        Metric,
        id=metric_id
    )

    entries = metric.entries.all()

    latest_entry = entries.first()

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

    chart_entries = entries.order_by('recorded_at', 'created_at')

    chart_labels = [
        entry.recorded_at.strftime('%b %d, %Y')
        for entry in chart_entries
    ]

    chart_values = [
        float(entry.value)
        for entry in chart_entries
    ]

    chart_target_values = []

    if metric.target_value is not None:

        chart_target_values = [
            float(metric.target_value)
            for entry in chart_entries
        ]

    context = {
        'metric': metric,
        'entries': entries,
        'latest_entry': latest_entry,
        'chart_labels': chart_labels,
        'chart_values': chart_values,
        'chart_target_values': chart_target_values,
        'performance_status': performance_status,
    }

    return render(
        request,
        'performance/metric_detail.html',
        context
    )


def data_entry_create(request, metric_id):

    metric = get_object_or_404(
        Metric,
        id=metric_id
    )

    if request.method == 'POST':

        form = DataEntryForm(request.POST)

        if form.is_valid():

            entry = form.save(commit=False)
            entry.metric = metric
            entry.save()

            return redirect(
                'performance:metric_detail',
                metric_id=metric.id
            )

    else:
        form = DataEntryForm()

    context = {
        'metric': metric,
        'form': form,
    }

    return render(
        request,
        'performance/data_entry_form.html',
        context
    )


def data_entry_update(request, entry_id):

    entry = get_object_or_404(
        DataEntry,
        id=entry_id
    )

    metric = entry.metric

    if request.method == 'POST':

        form = DataEntryForm(
            request.POST,
            instance=entry
        )

        if form.is_valid():

            form.save()

            return redirect(
                'performance:metric_detail',
                metric_id=metric.id
            )

    else:
        form = DataEntryForm(instance=entry)

    context = {
        'metric': metric,
        'form': form,
        'entry': entry,
    }

    return render(
        request,
        'performance/data_entry_form.html',
        context
    )


def data_entry_delete(request, entry_id):

    entry = get_object_or_404(
        DataEntry,
        id=entry_id
    )

    metric_id = entry.metric.id

    if request.method == 'POST':

        entry.delete()

        return redirect(
            'performance:metric_detail',
            metric_id=metric_id
        )

    context = {
        'entry': entry,
        'metric': entry.metric,
    }

    return render(
        request,
        'performance/data_entry_confirm_delete.html',
        context
    )


def metric_create(request, project_id):

    from projects.models import Project

    project = get_object_or_404(
        Project,
        id=project_id
    )

    if request.method == 'POST':

        form = MetricForm(request.POST)

        if form.is_valid():

            metric = form.save(commit=False)
            metric.project = project
            metric.save()

            return redirect(
                'performance:metric_detail',
                metric_id=metric.id
            )

    else:
        form = MetricForm()

    context = {
        'project': project,
        'form': form,
    }

    return render(
        request,
        'performance/metric_form.html',
        context
    )


def metric_update(request, metric_id):

    metric = get_object_or_404(
        Metric,
        id=metric_id
    )

    if request.method == 'POST':

        form = MetricForm(
            request.POST,
            instance=metric
        )

        if form.is_valid():

            form.save()

            return redirect(
                'performance:metric_detail',
                metric_id=metric.id
            )

    else:
        form = MetricForm(instance=metric)

    context = {
        'metric': metric,
        'project': metric.project,
        'form': form,
    }

    return render(
        request,
        'performance/metric_form.html',
        context
    )


def metric_delete(request, metric_id):

    metric = get_object_or_404(
        Metric,
        id=metric_id
    )

    project_id = metric.project.id

    if request.method == 'POST':

        metric.delete()

        return redirect(
            'project_detail',
            project_id=project_id
        )

    context = {
        'metric': metric,
    }

    return render(
        request,
        'performance/metric_confirm_delete.html',
        context
    )