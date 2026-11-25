from django import forms

from .models import DataEntry, Metric


class DataEntryForm(forms.ModelForm):

    class Meta:
        model = DataEntry

        fields = [
            'value',
            'recorded_at',
            'notes',
        ]

        widgets = {
            'value': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'placeholder': 'Enter measurement value',
            }),

            'recorded_at': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
            }),

            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Optional measurement notes',
            }),
        }


class MetricForm(forms.ModelForm):

    class Meta:
        model = Metric

        fields = [
            'name',
            'description',
            'direction',
            'unit',
            'baseline_value',
            'target_value',
        ]

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter metric name',
            }),

            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Describe what this metric measures',
            }),

            'direction': forms.Select(attrs={
                'class': 'form-select',
            }),

            'unit': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. %, hours, units',
            }),

            'baseline_value': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'placeholder': 'Enter baseline value',
            }),

            'target_value': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'placeholder': 'Enter target value',
            }),
        }