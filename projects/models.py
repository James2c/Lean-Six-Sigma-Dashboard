from django.db import models


class Project(models.Model):

    STATUS_CHOICES = [
        ('Planning', 'Planning'),
        ('In Progress', 'In Progress'),
        ('On Hold', 'On Hold'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ]

    PRIORITY_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
        ('Critical', 'Critical'),
    ]

    # Basic Information
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    # Lean Six Sigma Project Definition
    problem_statement = models.TextField(blank=True)
    goal_statement = models.TextField(blank=True)
    scope = models.TextField(blank=True)

    # Project Management
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Planning'
    )

    priority = models.CharField(
        max_length=20,
        choices=PRIORITY_CHOICES,
        default='Medium'
    )

    # Project Timeline
    start_date = models.DateField(null=True, blank=True)
    target_completion_date = models.DateField(null=True, blank=True)
    actual_completion_date = models.DateField(null=True, blank=True)

    # Recordkeeping
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class ProjectGoal(models.Model):

    DIRECTION_CHOICES = [
        ('Increase', 'Increase'),
        ('Decrease', 'Decrease'),
        ('Maintain', 'Maintain'),
    ]

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='goals'
    )

    name = models.CharField(max_length=200)

    description = models.TextField(blank=True)

    # Measurement Direction
    direction = models.CharField(
        max_length=20,
        choices=DIRECTION_CHOICES,
        default='Decrease'
    )

    # Performance Targets
    baseline_value = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    target_value = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    unit = models.CharField(
        max_length=50,
        default='%'
    )

    target_date = models.DateField(
        null=True,
        blank=True
    )

    # Recordkeeping
    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['target_date', 'name']

    def __str__(self):
        return f"{self.project.name} - {self.name}"