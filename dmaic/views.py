from dataclasses import dataclass
from typing import Any

from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from projects.models import Project
from .models import DMAICPhase, PhaseDeliverable
from .services import initialize_dmaic_phases
from .forms import DMAICPhaseForm, PhaseDeliverableForm


@dataclass
class DMAICPhaseProgress:

    phase: DMAICPhase

    total_deliverables: int

    not_started_deliverables: int

    in_progress_deliverables: int

    completed_deliverables: int

    deliverable_progress: float

    not_started_progress: float

    in_progress_progress: float

    overdue_deliverables: int



def dmaic_project_list(request):

    projects = Project.objects.all()

    context = {
        'projects': projects,
    }

    return render(
        request,
        'dmaic/dmaic_project_list.html',
        context
    )



def dmaic_workspace(request, project_id):

    project = get_object_or_404(
        Project,
        id=project_id
    )

    # Ensure all five DMAIC phases exist
    initialize_dmaic_phases(project)

    phases = DMAICPhase.objects.filter(
        project=project
    )

    phase_progress_list = []

    for phase in phases:

        total_deliverables = phase.deliverables.count()

        completed_deliverables = phase.deliverables.filter(
            status='Completed'
        ).count()

        not_started_deliverables = phase.deliverables.filter(
            status='Not Started'
        ).count()

        in_progress_deliverables = phase.deliverables.filter(
            status='In Progress'
        ).count()

        overdue_deliverables = phase.deliverables.filter(
            due_date__lt=timezone.localdate()
        ).exclude(
            status='Completed'
        ).count()

        deliverable_progress = (
            (completed_deliverables / total_deliverables) * 100
            if total_deliverables > 0
            else 0
        )

        not_started_progress = (
            (not_started_deliverables / total_deliverables) * 100
            if total_deliverables > 0
            else 0
        )

        in_progress_progress = (
            (in_progress_deliverables / total_deliverables) * 100
            if total_deliverables > 0
            else 0
        )

        phase_progress_list.append(
            DMAICPhaseProgress(
                phase=phase,
                total_deliverables=total_deliverables,
                completed_deliverables=completed_deliverables,
                deliverable_progress=deliverable_progress,
                overdue_deliverables=overdue_deliverables,
                not_started_deliverables=not_started_deliverables,
                in_progress_deliverables=in_progress_deliverables,
                not_started_progress=not_started_progress,
                in_progress_progress=in_progress_progress,
            )
        )

    # Overall deliverable progress
    total_deliverables = sum(
        item.total_deliverables
        for item in phase_progress_list
    )

    completed_deliverables = sum(
        item.completed_deliverables
        for item in phase_progress_list
    )

    total_not_started_deliverables = sum(
        item.not_started_deliverables
        for item in phase_progress_list
    )

    total_in_progress_deliverables = sum(
        item.in_progress_deliverables
        for item in phase_progress_list
    )

    not_started_progress = (
        (total_not_started_deliverables / total_deliverables) * 100
        if total_deliverables > 0
        else 0
    )

    in_progress_progress = (
        (total_in_progress_deliverables / total_deliverables) * 100
        if total_deliverables > 0
        else 0
    )

    deliverable_progress = (
        (completed_deliverables / total_deliverables) * 100
        if total_deliverables > 0
        else 0
    )

    total_overdue_deliverables = sum(
                item.overdue_deliverables
                for item in phase_progress_list
            )

    # DMAIC phase progress
    total_phases = phases.count()

    completed_phases = phases.filter(
        status='Completed'
    ).count()

    in_progress_phases = phases.filter(
        status='In Progress'
    ).count()

    progress_percentage = (
        (completed_phases / total_phases) * 100
        if total_phases > 0
        else 0
    )

    context = {
        'project': project,
        'phases': phases,
        'phase_progress_list': phase_progress_list,
        'total_phases': total_phases,
        'completed_phases': completed_phases,
        'in_progress_phases': in_progress_phases,
        'progress_percentage': progress_percentage,
        'total_deliverables': total_deliverables,
        'completed_deliverables': completed_deliverables,
        'deliverable_progress': deliverable_progress,
        'not_started_progress': not_started_progress,
        'in_progress_progress': in_progress_progress,
        'total_overdue_deliverables': total_overdue_deliverables,
        'total_not_started_deliverables': total_not_started_deliverables,
        'total_in_progress_deliverables': total_in_progress_deliverables,
    }

    return render(
        request,
        'dmaic/dmaic_workspace.html',
        context
    )


def dmaic_phase_detail(request, project_id, phase_id):

    project = get_object_or_404(
        Project,
        id=project_id
    )

    phase = get_object_or_404(
        DMAICPhase,
        id=phase_id,
        project=project
    )

    deliverables = phase.deliverables.all()

    today = timezone.localdate()

    overdue_deliverables = deliverables.filter(
        due_date__lt=today
    ).exclude(
        status='Completed'
    )

    overdue_count = overdue_deliverables.count()

    total_deliverables = deliverables.count()

    completed_deliverables = deliverables.filter(
        status='Completed'
    ).count()

    deliverable_progress = (
        (completed_deliverables / total_deliverables) * 100
        if total_deliverables > 0
        else 0
    )

    if request.method == 'POST':

        form = DMAICPhaseForm(
            request.POST,
            instance=phase
        )

        if form.is_valid():

            updated_phase = form.save(commit=False)

            # Prevent phase completion with unfinished deliverables
            if (
                updated_phase.status == 'Completed'
                and updated_phase.deliverables.exclude(
                    status='Completed'
                ).exists()
            ):
                form.add_error(
                    None,
                    'This phase cannot be completed until all deliverables are marked Completed.'
                )

                # Restore the saved phase values for the page context
                phase.refresh_from_db()

            else:

                today = timezone.localdate()

                # Automatically set start date
                if (
                    updated_phase.status in ['In Progress', 'Completed']
                    and not updated_phase.start_date
                ):
                    updated_phase.start_date = today

                # Automatically set completion date
                if (
                    updated_phase.status == 'Completed'
                    and not updated_phase.completion_date
                ):
                    updated_phase.completion_date = today

                updated_phase.save()

                return redirect(
                    'dmaic_phase_detail',
                    project_id=project.id,
                    phase_id=phase.id
                )

    else:

        form = DMAICPhaseForm(
            instance=phase
        )

    context = {
        'project': project,
        'phase': phase,
        'form': form,
        'deliverables': deliverables,
        'total_deliverables': total_deliverables,
        'completed_deliverables': completed_deliverables,
        'deliverable_progress': deliverable_progress,
        'today': today,
        'overdue_deliverables': overdue_deliverables,
        'overdue_count': overdue_count,
    }

    return render(
        request,
        'dmaic/dmaic_phase_detail.html',
        context
    )


def update_phase_status(phase):

    total_deliverables = phase.deliverables.count()

    completed_deliverables = phase.deliverables.filter(
        status='Completed'
    ).count()

    in_progress_deliverables = phase.deliverables.filter(
        status='In Progress'
    ).exists()

    # All deliverables completed
    if (
        total_deliverables > 0
        and completed_deliverables == total_deliverables
    ):
        phase.status = 'Completed'

        if not phase.completion_date:
            phase.completion_date = timezone.localdate()

    # At least one unfinished deliverable in a completed phase
    elif phase.status == 'Completed':
        phase.status = 'In Progress'
        phase.completion_date = None

    # At least one deliverable in progress
    elif in_progress_deliverables:
        phase.status = 'In Progress'

    phase.save()


def deliverable_create(request, project_id, phase_id):

    project = get_object_or_404(
        Project,
        id=project_id
    )

    phase = get_object_or_404(
        DMAICPhase,
        id=phase_id,
        project=project
    )

    if request.method == 'POST':

        form = PhaseDeliverableForm(request.POST)

        if form.is_valid():

            deliverable = form.save(commit=False)
            deliverable.phase = phase

            if deliverable.status == 'Completed':
                deliverable.completed_at = timezone.localdate()

            deliverable.save()

            update_phase_status(phase)

            return redirect(
                'dmaic_phase_detail',
                project_id=project.id,
                phase_id=phase.id
            )

    else:

        form = PhaseDeliverableForm()

    return render(
        request,
        'dmaic/deliverable_form.html',
        {
            'project': project,
            'phase': phase,
            'form': form,
            'is_edit': False,
        }
    )



def deliverable_edit(request, project_id, phase_id, deliverable_id):

    project = get_object_or_404(
        Project,
        id=project_id
    )

    phase = get_object_or_404(
        DMAICPhase,
        id=phase_id,
        project=project
    )

    deliverable = get_object_or_404(
        PhaseDeliverable,
        id=deliverable_id,
        phase=phase
    )

    if request.method == 'POST':

        form = PhaseDeliverableForm(
            request.POST,
            instance=deliverable
        )

        if form.is_valid():

            updated_deliverable = form.save(commit=False)

            if (
                updated_deliverable.status == 'Completed'
                and not updated_deliverable.completed_at
            ):
                updated_deliverable.completed_at = timezone.localdate()

            updated_deliverable.save()

            update_phase_status(phase)

            return redirect(
                'dmaic_phase_detail',
                project_id=project.id,
                phase_id=phase.id
            )

    else:

        form = PhaseDeliverableForm(
            instance=deliverable
        )

    return render(
        request,
        'dmaic/deliverable_form.html',
        {
            'project': project,
            'phase': phase,
            'deliverable': deliverable,
            'form': form,
            'is_edit': True,
        }
    )


def deliverable_delete(request, project_id, phase_id, deliverable_id):

    project = get_object_or_404(
        Project,
        id=project_id
    )

    phase = get_object_or_404(
        DMAICPhase,
        id=phase_id,
        project=project
    )

    deliverable = get_object_or_404(
        PhaseDeliverable,
        id=deliverable_id,
        phase=phase
    )

    if request.method == 'POST':

        deliverable.delete()

        # Update phase status if deliverables remain
        if phase.deliverables.exists():
            update_phase_status(phase)

        return redirect(
            'dmaic_phase_detail',
            project_id=project.id,
            phase_id=phase.id
        )

    return render(
        request,
        'dmaic/deliverable_confirm_delete.html',
        {
            'project': project,
            'phase': phase,
            'deliverable': deliverable,
        }
    )
