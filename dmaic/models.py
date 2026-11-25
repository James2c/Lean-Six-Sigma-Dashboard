from django.db import models
from projects.models import Project


class DMAICPhase(models.Model):

    PHASE_CHOICES = [
        ('Define', 'Define'),
        ('Measure', 'Measure'),
        ('Analyze', 'Analyze'),
        ('Improve', 'Improve'),
        ('Control', 'Control'),
    ]

    STATUS_CHOICES = [
        ('Not Started', 'Not Started'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
    ]

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='dmaic_phases'
    )

    phase = models.CharField(
        max_length=20,
        choices=PHASE_CHOICES
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Not Started'
    )

    start_date = models.DateField(
        null=True,
        blank=True
    )

    completion_date = models.DateField(
        null=True,
        blank=True
    )

    notes = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['id']
        constraints = [
            models.UniqueConstraint(
                fields=['project', 'phase'],
                name='unique_dmaic_phase_per_project'
            )
        ]

    def __str__(self):
        return f"{self.project.name} - {self.phase}"



class PhaseDeliverable(models.Model):

    STATUS_CHOICES = [
        ('Not Started', 'Not Started'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
    ]

    phase = models.ForeignKey(
        DMAICPhase,
        on_delete=models.CASCADE,
        related_name='deliverables'
    )

    name = models.CharField(
        max_length=200
    )

    description = models.TextField(
        blank=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Not Started'
    )

    due_date = models.DateField(
        null=True,
        blank=True
    )

    completed_at = models.DateField(
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"{self.phase.phase} - {self.name}"

