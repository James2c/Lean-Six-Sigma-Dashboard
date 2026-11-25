from django.contrib import admin
from .models import Risk


@admin.register(Risk)
class RiskAdmin(admin.ModelAdmin):

    list_display = (
        'title',
        'project',
        'category',
        'likelihood',
        'impact',
        'risk_score',
        'risk_level',
        'status',
        'owner',
    )

    list_filter = (
        'category',
        'status',
        'likelihood',
        'impact',
    )

    search_fields = (
        'title',
        'description',
        'project__name',
        'owner',
    )

    readonly_fields = (
        'created_at',
        'updated_at',
    )