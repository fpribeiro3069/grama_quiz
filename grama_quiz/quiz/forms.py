from django import forms
from .models import Team

class TeamForm(forms.Form):
    name = forms.CharField(
        max_length=100, 
        widget=forms.TextInput(attrs={'class': 'team-form'}),
        label='Nome da Equipa')
    
    def clean_name(self):
        name = self.cleaned_data.get('name')
        if Team.objects.filter(name=name).exists():
            raise forms.ValidationError("Já existe uma equipa com esse nome")
        return name