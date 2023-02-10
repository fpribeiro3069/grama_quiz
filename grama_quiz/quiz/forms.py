from django import forms

class TeamForm(forms.Form):
    name = forms.CharField(
        max_length=100, 
        widget=forms.TextInput(attrs={'class': 'team-form'}),
        label='Nome da Equipa')