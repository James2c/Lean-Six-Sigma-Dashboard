from django import forms
from .models import Project


class ProjectForm(forms.ModelForm):

    class Meta:
        model = Project

        fields = [
            'name',
            'description',
            'problem_statement',
            'goal_statement',
            'scope',
            'status',
            'priority',
            'start_date',
            'target_completion_date',
        ]

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter project name',
            }),

            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Brief project overview',
            }),

            'problem_statement': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
            }),

            'goal_statement': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
            }),

            'scope': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
            }),

            'status': forms.Select(attrs={
                'class': 'form-select',
            }),

            'priority': forms.Select(attrs={
                'class': 'form-select',
            }),

            'start_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
            }),

            'target_completion_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
            }),
        }