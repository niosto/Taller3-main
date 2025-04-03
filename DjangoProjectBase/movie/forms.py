from django import forms

class PromptForm(forms.Form):
    prompt = forms.CharField(
        label='Describe lo que buscas',
        widget=forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
        max_length=1000,
        required=True
    )