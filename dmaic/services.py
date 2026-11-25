from .models import DMAICPhase


def initialize_dmaic_phases(project):

    phases = [
        'Define',
        'Measure',
        'Analyze',
        'Improve',
        'Control',
    ]

    for phase in phases:
        DMAICPhase.objects.get_or_create(
            project=project,
            phase=phase,
        )
