from django.db import models
from projects.models import Project
from django.utils import timezone


class Metric(models.Model):

    DIRECTION_CHOICES = [
        ('Increase', 'Increase'),
        ('Decrease', 'Decrease'),
        ('Maintain', 'Maintain'),
    ]

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='metrics'
    )

    name = models.CharField(max_length=200)

    description = models.TextField(blank=True)

    unit = models.CharField(
        max_length=50,
        default='%'
    )

    direction = models.CharField(
        max_length=20,
        choices=DIRECTION_CHOICES,
        default='Decrease'
    )

    baseline_value = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True
    )

    target_value = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.project.name} - {self.name}"


class DataEntry(models.Model):

    metric = models.ForeignKey(
        Metric,
        on_delete=models.CASCADE,
        related_name='entries'
    )

    value = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    recorded_at = models.DateField(
        default=timezone.localdate
    )

    notes = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-recorded_at', '-created_at']

    def __str__(self):
        return f"{self.metric.name} - {self.value} ({self.recorded_at})"