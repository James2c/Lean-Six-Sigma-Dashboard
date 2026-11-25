from django.shortcuts import get_object_or_404, redirect, render

from .forms import RiskForm
from projects.models import Project


def risk_list(request, project_id):

    project = get_object_or_404(
        Project,
        id=project_id
    )

    risks = project.risks.all()

    context = {
        'project': project,
        'risks': risks,
    }

    return render(
        request,
        'risk/risk_list.html',
        context
    )


def risk_create(request, project_id):

    project = get_object_or_404(
        Project,
        id=project_id
    )

    if request.method == 'POST':
        form = RiskForm(request.POST)

        if form.is_valid():
            risk = form.save(commit=False)
            risk.project = project
            risk.save()

            return redirect(
                'risk_list',
                project_id=project.id
            )

    else:
        form = RiskForm()

    context = {
        'project': project,
        'form': form,
    }

    return render(
        request,
        'risk/risk_form.html',
        context
    )


def risk_edit(request, project_id, risk_id):

    project = get_object_or_404(
        Project,
        id=project_id
    )

    risk = get_object_or_404(
        project.risks,
        id=risk_id
    )

    if request.method == 'POST':
        form = RiskForm(request.POST, instance=risk)

        if form.is_valid():
            form.save()

            return redirect(
                'risk_detail',
                project_id=project.id,
                risk_id=risk.id
            )

    else:
        form = RiskForm(instance=risk)

    context = {
        'project': project,
        'risk': risk,
        'form': form,
        'is_edit': True,
    }

    return render(
        request,
        'risk/risk_form.html',
        context
    )


def risk_delete(request, project_id, risk_id):

    project = get_object_or_404(
        Project,
        id=project_id
    )

    risk = get_object_or_404(
        project.risks,
        id=risk_id
    )

    if request.method == 'POST':
        risk.delete()

        return redirect(
            'risk_list',
            project_id=project.id
        )

    context = {
        'project': project,
        'risk': risk,
    }

    return render(
        request,
        'risk/risk_confirm_delete.html',
        context
    )


def risk_detail(request, project_id, risk_id):

    project = get_object_or_404(
        Project,
        id=project_id
    )

    risk = get_object_or_404(
        project.risks,
        id=risk_id
    )

    context = {
        'project': project,
        'risk': risk,
    }

    return render(
        request,
        'risk/risk_detail.html',
        context
    )


def risk_matrix(request, project_id):

    project = get_object_or_404(
        Project,
        id=project_id
    )

    risks = project.risks.exclude(
        status='Closed'
    )

    risk_lookup = {}

    for risk in risks:
        key = (risk.likelihood, risk.impact)

        if key not in risk_lookup:
            risk_lookup[key] = []

        risk_lookup[key].append(risk)

    matrix_rows = []

    for likelihood in range(5, 0, -1):

        row = []

        for impact in range(1, 6):

            score = likelihood * impact

            if score <= 4:
                level = 'Low'
                color = 'bg-success'

            elif score <= 9:
                level = 'Moderate'
                color = 'bg-info'

            elif score <= 16:
                level = 'High'
                color = 'bg-warning'

            else:
                level = 'Critical'
                color = 'bg-danger'

            row.append({
                'likelihood': likelihood,
                'impact': impact,
                'score': score,
                'level': level,
                'color': color,
                'risks': risk_lookup.get(
                    (likelihood, impact),
                    []
                ),
            })

        matrix_rows.append({
            'likelihood': likelihood,
            'cells': row,
        })

    context = {
        'project': project,
        'matrix_rows': matrix_rows,
    }

    return render(
        request,
        'risk/risk_matrix.html',
        context
    )