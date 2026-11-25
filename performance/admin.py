from django.contrib import admin
from .models import Metric, DataEntry


@admin.register(Metric)
class MetricAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'project',
        'direction',
        'baseline_value',
        'target_value',
        'unit',
    )

    list_filter = (
        'direction',
        'project',
    )

    search_fields = (
        'name',
        'project__name',
    )

    ordering = (
        'project',
        'name',
    )


@admin.register(DataEntry)
class DataEntryAdmin(admin.ModelAdmin):

    list_display = (
        'metric',
        'value',
        'recorded_at',
        'created_at',
    )

    list_filter = (
        'recorded_at',
        'metric',
    )

    search_fields = (
        'metric__name',
        'notes',
    )

    ordering = (
        '-recorded_at',
    )