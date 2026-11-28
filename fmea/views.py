from django.shortcuts import render, get_object_or_404, redirect

from projects.models import Project
from .models import FailureMode, CorrectiveAction
from .forms import FailureModeForm, CorrectiveActionForm


def fmea_dashboard(request, project_id):

    project = get_object_or_404(
        Project,
        id=project_id
    )

    failure_modes = FailureMode.objects.filter(
        project=project
    ).prefetch_related(
        'corrective_actions'
    )

    corrective_actions = CorrectiveAction.objects.filter(
        failure_mode__project=project
    )

    context_total = corrective_actions.count()

    context_completed = corrective_actions.filter(
        status='Completed'
    ).count()

    context_verified = corrective_actions.filter(
        effectiveness_verified=True
    ).count()

    context = {
        'project': project,
        'failure_modes': failure_modes,
        'corrective_actions': corrective_actions,

        'total_failure_modes': failure_modes.count(),

        'critical_failure_modes': sum(
            1 for failure in failure_modes
            if failure.risk_level == 'Critical'
        ),

        'total_corrective_actions': corrective_actions.count(),

        'open_corrective_actions': corrective_actions.filter(
            status='Open'
        ).count(),

        'completed_corrective_actions': corrective_actions.filter(
            status='Completed'
        ).count(),

        'overdue_corrective_actions': sum(
            1 for action in corrective_actions if action.is_overdue
        ),

        'corrective_action_completion': round(
            (
                context_completed / context_total * 100
            ) if context_total else 0
        ),

        'effectiveness_verification_percentage': round(
            (
                context_verified / context_total * 100
            ) if context_total else 0
        ),

        'verified_corrective_actions': context_verified,
    }

    return render(
        request,
        'fmea/fmea_dashboard.html',
        context
    )


def failure_mode_create(request, project_id):

    project = get_object_or_404(
        Project,
        id=project_id
    )

    if request.method == 'POST':

        form = FailureModeForm(request.POST)

        if form.is_valid():

            failure_mode = form.save(commit=False)

            failure_mode.project = project

            failure_mode.save()

            return redirect(
                'fmea_dashboard',
                project_id=project.id
            )

    else:

        form = FailureModeForm()

    context = {
        'project': project,
        'form': form,
    }

    return render(
        request,
        'fmea/failure_mode_form.html',
        context
    )


def failure_mode_edit(request, project_id, failure_id):

    project = get_object_or_404(
        Project,
        id=project_id
    )

    failure_mode = get_object_or_404(
        FailureMode,
        id=failure_id,
        project=project
    )

    if request.method == 'POST':

        form = FailureModeForm(
            request.POST,
            instance=failure_mode
        )

        if form.is_valid():

            form.save()

            return redirect(
                'fmea_dashboard',
                project_id=project.id
            )

    else:

        form = FailureModeForm(
            instance=failure_mode
        )

    context = {
        'project': project,
        'form': form,
        'failure_mode': failure_mode,
        'is_edit': True,
    }

    return render(
        request,
        'fmea/failure_mode_form.html',
        context
    )


def failure_mode_detail(request, project_id, failure_id):

    project = get_object_or_404(
        Project,
        id=project_id
    )

    failure_mode = get_object_or_404(
        FailureMode.objects.prefetch_related(
            'corrective_actions'
        ),
        id=failure_id,
        project=project
    )

    corrective_actions = failure_mode.corrective_actions.all()

    total_actions = corrective_actions.count()
    completed_actions = corrective_actions.filter(status='Completed').count()

    completion_percentage = (
        round((completed_actions / total_actions) * 100)
        if total_actions > 0
        else 0
    )

    verified_actions = corrective_actions.filter(
        effectiveness_verified=True
    ).count()

    verification_percentage = (
        round((verified_actions / total_actions) * 100)
        if total_actions > 0
        else 0
    )

    context = {
        'project': project,
        'failure_mode': failure_mode,
        'corrective_actions': corrective_actions,
        'total_corrective_actions': corrective_actions.count(),
        'open_corrective_actions': corrective_actions.filter(
            status='Open'
        ).count(),
        'completed_corrective_actions': corrective_actions.filter(
            status='Completed'
        ).count(),
        'overdue_corrective_actions': sum(
            1 for action in corrective_actions if action.is_overdue
        ),
        'verified_corrective_actions': corrective_actions.filter(
            effectiveness_verified=True
        ).count(),
        'completion_percentage': completion_percentage,
        'verification_percentage': verification_percentage,
    }

    return render(
        request,
        'fmea/failure_mode_detail.html',
        context
    )


def corrective_action_create(request, project_id, failure_id):

    project = get_object_or_404(Project, id=project_id)

    failure_mode = get_object_or_404(
        FailureMode,
        id=failure_id,
        project=project
    )

    if request.method == 'POST':
        form = CorrectiveActionForm(request.POST)

        if form.is_valid():
            corrective_action = form.save(commit=False)
            corrective_action.failure_mode = failure_mode
            corrective_action.save()

            return redirect(
                'failure_mode_detail',
                project_id=project.id,
                failure_id=failure_mode.id
            )

    else:
        form = CorrectiveActionForm()

    context = {
        'project': project,
        'failure_mode': failure_mode,
        'form': form,
    }

    return render(
        request,
        'fmea/corrective_action_form.html',
        context
    )


def corrective_action_edit(request, project_id, failure_id, action_id):

    project = get_object_or_404(Project, id=project_id)

    failure_mode = get_object_or_404(
        FailureMode,
        id=failure_id,
        project=project
    )

    corrective_action = get_object_or_404(
        CorrectiveAction,
        id=action_id,
        failure_mode=failure_mode
    )

    if request.method == 'POST':
        form = CorrectiveActionForm(
            request.POST,
            instance=corrective_action
        )

        if form.is_valid():
            form.save()

            return redirect(
                'failure_mode_detail',
                project_id=project.id,
                failure_id=failure_mode.id
            )

    else:
        form = CorrectiveActionForm(instance=corrective_action)

    context = {
        'project': project,
        'failure_mode': failure_mode,
        'corrective_action': corrective_action,
        'form': form,
        'is_edit': True,
    }

    return render(
        request,
        'fmea/corrective_action_form.html',
        context
    )


def corrective_action_delete(request, project_id, failure_id, action_id):

    project = get_object_or_404(Project, id=project_id)

    failure_mode = get_object_or_404(
        FailureMode,
        id=failure_id,
        project=project
    )

    corrective_action = get_object_or_404(
        CorrectiveAction,
        id=action_id,
        failure_mode=failure_mode
    )

    if request.method == 'POST':
        corrective_action.delete()

        return redirect(
            'failure_mode_detail',
            project_id=project.id,
            failure_id=failure_mode.id
        )

    context = {
        'project': project,
        'failure_mode': failure_mode,
        'corrective_action': corrective_action,
    }

    return render(
        request,
        'fmea/corrective_action_confirm_delete.html',
        context
    )