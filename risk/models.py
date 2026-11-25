from django.db import models
from django.utils import timezone
from projects.models import Project


class Risk(models.Model):

    CATEGORY_CHOICES = [
        ('Operational', 'Operational'),
        ('Financial', 'Financial'),
        ('Quality', 'Quality'),
        ('Safety', 'Safety'),
        ('Technical', 'Technical'),
        ('Environmental', 'Environmental'),
        ('Other', 'Other'),
    ]

    STATUS_CHOICES = [
        ('Open', 'Open'),
        ('In Progress', 'In Progress'),
        ('Mitigated', 'Mitigated'),
        ('Closed', 'Closed'),
    ]

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='risks'
    )

    title = models.CharField(max_length=200)

    description = models.TextField()

    category = models.CharField(
        max_length=30,
        choices=CATEGORY_CHOICES,
        default='Operational'
    )

    likelihood = models.PositiveSmallIntegerField(
        choices=[(i, str(i)) for i in range(1, 6)],
        default=3
    )

    impact = models.PositiveSmallIntegerField(
        choices=[(i, str(i)) for i in range(1, 6)],
        default=3
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Open'
    )

    mitigation_plan = models.TextField(blank=True)

    owner = models.CharField(
        max_length=150,
        blank=True
    )

    identified_date = models.DateField(
        default=timezone.localdate
    )

    target_resolution_date = models.DateField(
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.project.name} - {self.title}"

    @property
    def risk_score(self):
        return self.likelihood * self.impact

    @property
    def risk_level(self):

        score = self.risk_score

        if score <= 4:
            return 'Low'
        elif score <= 9:
            return 'Moderate'
        elif score <= 16:
            return 'High'
        else:
            return 'Critical'