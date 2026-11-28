from django.db import models
from projects.models import Project


class FailureMode(models.Model):

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='failure_modes'
    )

    process_step = models.CharField(
        max_length=200
    )

    failure_mode = models.CharField(
        max_length=250
    )

    failure_effect = models.TextField()

    failure_cause = models.TextField()

    prevention_controls = models.TextField(
        blank=True
    )

    detection_controls = models.TextField(
        blank=True
    )

    severity = models.PositiveSmallIntegerField(
        choices=[(i, str(i)) for i in range(1, 11)],
        default=5
    )

    occurrence = models.PositiveSmallIntegerField(
        choices=[(i, str(i)) for i in range(1, 11)],
        default=5
    )

    detection = models.PositiveSmallIntegerField(
        choices=[(i, str(i)) for i in range(1, 11)],
        default=5
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.project.name} - {self.failure_mode}"

    @property
    def rpn(self):
        return self.severity * self.occurrence * self.detection

    @property
    def risk_level(self):

        if self.rpn >= 500:
            return 'Critical'

        elif self.rpn >= 250:
            return 'High'

        elif self.rpn >= 100:
            return 'Moderate'

        else:
            return 'Low'


class CorrectiveAction(models.Model):

    STATUS_CHOICES = [
        ('Open', 'Open'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ]

    failure_mode = models.ForeignKey(
        FailureMode,
        on_delete=models.CASCADE,
        related_name='corrective_actions'
    )

    action_description = models.TextField()

    assigned_to = models.CharField(
        max_length=150,
        blank=True
    )

    due_date = models.DateField(
        null=True,
        blank=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Open'
    )

    completion_date = models.DateField(
        null=True,
        blank=True
    )

    effectiveness_verified = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ['due_date', '-created_at']

    def __str__(self):
        return f"Action for {self.failure_mode.failure_mode}"

    @property
    def is_overdue(self):
        from django.utils import timezone

        return (
            self.due_date is not None
            and self.due_date < timezone.localdate()
            and self.status not in ['Completed', 'Cancelled']
        )