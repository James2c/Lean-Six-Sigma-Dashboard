from django import forms
from .models import FailureMode, CorrectiveAction


class FailureModeForm(forms.ModelForm):

    class Meta:
        model = FailureMode

        fields = [
            'process_step',
            'failure_mode',
            'failure_effect',
            'failure_cause',
            'prevention_controls',
            'detection_controls',
            'severity',
            'occurrence',
            'detection',
        ]

        widgets = {
            'process_step': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter process step'
            }),

            'failure_mode': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Describe potential failure'
            }),

            'failure_effect': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3
            }),

            'failure_cause': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3
            }),

            'prevention_controls': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3
            }),

            'detection_controls': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3
            }),

            'severity': forms.Select(attrs={
                'class': 'form-select'
            }),

            'occurrence': forms.Select(attrs={
                'class': 'form-select'
            }),

            'detection': forms.Select(attrs={
                'class': 'form-select'
            }),

            'severity': forms.Select(attrs={
                'class': 'form-select'
            }),

            'occurrence': forms.Select(attrs={
                'class': 'form-select'
            }),

            'detection': forms.Select(attrs={
                'class': 'form-select'
            }),
        }

        help_texts = {
            'severity': '1 = Negligible impact, 10 = Extremely severe impact.',
            'occurrence': '1 = Extremely unlikely, 10 = Very frequent.',
            'detection': '1 = Almost certain to detect, 10 = Almost impossible to detect.',
        }


class CorrectiveActionForm(forms.ModelForm):

    class Meta:
        model = CorrectiveAction

        fields = [
            'action_description',
            'assigned_to',
            'due_date',
            'status',
            'completion_date',
            'effectiveness_verified',
        ]

        widgets = {
            'action_description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
            }),

            'assigned_to': forms.TextInput(attrs={
                'class': 'form-control',
            }),

            'due_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
            }),

            'status': forms.Select(attrs={
                'class': 'form-select',
            }),

            'completion_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
            }),

            'effectiveness_verified': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
        }

    def clean(self):

        cleaned_data = super().clean()

        status = cleaned_data.get('status')
        completion_date = cleaned_data.get('completion_date')

        if status == 'Completed' and not completion_date:
            from django.utils import timezone

            cleaned_data['completion_date'] = timezone.localdate()

        elif status != 'Completed':
            cleaned_data['completion_date'] = None

        if cleaned_data.get('effectiveness_verified') and status != 'Completed':
            self.add_error(
                'effectiveness_verified',
                'A corrective action must be completed before its effectiveness can be verified.'
            )

        if (
            self.instance.pk
            and self.instance.effectiveness_verified
            and status != 'Completed'
        ):
            self.add_error(
                'status',
                'A verified corrective action cannot be reopened. Remove effectiveness verification first.'
            )

        return cleaned_data