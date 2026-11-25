from django import forms

from .models import Risk


class RiskForm(forms.ModelForm):

    class Meta:
        model = Risk

        fields = [
            'title',
            'description',
            'category',
            'likelihood',
            'impact',
            'status',
            'mitigation_plan',
            'owner',
            'identified_date',
            'target_resolution_date',
        ]

        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter risk title',
            }),

            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Describe the potential risk',
            }),

            'category': forms.Select(attrs={
                'class': 'form-select',
            }),

            'likelihood': forms.Select(attrs={
                'class': 'form-select',
            }),

            'impact': forms.Select(attrs={
                'class': 'form-select',
            }),

            'status': forms.Select(attrs={
                'class': 'form-select',
            }),

            'mitigation_plan': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Describe how this risk will be mitigated',
            }),

            'owner': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter responsible person',
            }),

            'identified_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
            }),

            'target_resolution_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
            }),
        }