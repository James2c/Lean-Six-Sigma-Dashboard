from django import forms
from .models import DMAICPhase, PhaseDeliverable


class DMAICPhaseForm(forms.ModelForm):

    class Meta:
        model = DMAICPhase

        fields = [
            'status',
            'start_date',
            'completion_date',
            'notes',
        ]

        widgets = {
            'status': forms.Select(attrs={
                'class': 'form-select',
            }),

            'start_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
            }),

            'completion_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
            }),

            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Enter phase notes, findings, or updates...',
            }),
        }



class PhaseDeliverableForm(forms.ModelForm):

    class Meta:
        model = PhaseDeliverable

        fields = [
            'name',
            'description',
            'status',
            'due_date',
        ]

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter deliverable name',
            }),

            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Describe the deliverable...',
            }),

            'status': forms.Select(attrs={
                'class': 'form-select',
            }),

            'due_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
            }),
        }
