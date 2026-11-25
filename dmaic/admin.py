
from django.contrib import admin
from .models import DMAICPhase, PhaseDeliverable


@admin.register(DMAICPhase)
class DMAICPhaseAdmin(admin.ModelAdmin):

    list_display = (
        'project',
        'phase',
        'status',
        'start_date',
        'completion_date',
    )

    list_filter = (
        'phase',
        'status',
    )

    search_fields = (
        'project__name',
        'notes',
    )

    ordering = (
        'project',
        'id',
    )


@admin.register(PhaseDeliverable)
class PhaseDeliverableAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'phase',
        'status',
        'due_date',
        'completed_at',
    )

    list_filter = (
        'status',
        'phase__phase',
    )

    search_fields = (
        'name',
        'description',
        'phase__project__name',
    )

    ordering = (
        'phase',
        'created_at',
    )
