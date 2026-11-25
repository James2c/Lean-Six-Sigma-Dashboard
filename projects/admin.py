from django.contrib import admin
from .models import Project, ProjectGoal


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'status',
        'priority',
        'start_date',
        'target_completion_date',
        'created_at',
    )

    list_filter = (
        'status',
        'priority',
    )

    search_fields = (
        'name',
        'description',
        'problem_statement',
        'goal_statement',
    )

    ordering = ('-created_at',)

    readonly_fields = (
        'created_at',
        'updated_at',
    )

    fieldsets = (
        ('Basic Information', {
            'fields': (
                'name',
                'description',
            )
        }),
        ('Project Definition', {
            'fields': (
                'problem_statement',
                'goal_statement',
                'scope',
            )
        }),
        ('Project Management', {
            'fields': (
                'status',
                'priority',
            )
        }),
        ('Project Timeline', {
            'fields': (
                'start_date',
                'target_completion_date',
                'actual_completion_date',
            )
        }),
        ('Recordkeeping', {
            'fields': (
                'created_at',
                'updated_at',
            )
        }),
    )


@admin.register(ProjectGoal)
class ProjectGoalAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'project',
        'direction',
        'baseline_value',
        'target_value',
        'unit',
        'target_date',
    )

    list_filter = (
        'direction',
        'target_date',
    )

    search_fields = (
        'name',
        'project__name',
    )

    ordering = (
        'target_date',
        'name',
    )
