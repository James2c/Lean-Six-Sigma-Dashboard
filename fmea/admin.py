from django.contrib import admin
from .models import FailureMode, CorrectiveAction


@admin.register(FailureMode)
class FailureModeAdmin(admin.ModelAdmin):

    list_display = (
        'project',
        'process_step',
        'failure_mode',
        'severity',
        'occurrence',
        'detection',
        'rpn',
        'risk_level',
    )

    list_filter = (
        'project',
        'severity',
        'occurrence',
        'detection',
    )

    search_fields = (
        'failure_mode',
        'process_step',
        'failure_cause',
        'failure_effect',
    )

    readonly_fields = (
        'created_at',
        'updated_at',
    )


@admin.register(CorrectiveAction)
class CorrectiveActionAdmin(admin.ModelAdmin):

    list_display = (
        'failure_mode',
        'assigned_to',
        'due_date',
        'status',
        'completion_date',
        'effectiveness_verified',
    )

    list_filter = (
        'status',
        'effectiveness_verified',
        'due_date',
    )

    search_fields = (
        'action_description',
        'assigned_to',
        'failure_mode__failure_mode',
    )

    readonly_fields = (
        'created_at',
        'updated_at',
    )