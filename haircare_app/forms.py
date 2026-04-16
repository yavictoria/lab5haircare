from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import HairProfile,JournalEntry
from django.contrib.auth.models import User

class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

class HairProfileForm(forms.ModelForm):
    class Meta:
        model = HairProfile
        fields = ['nickname', 'hair_type', 'hair_length', 'porosity', 'brittleness', 'dyed']

class JournalEntryForm(forms.ModelForm):
    class Meta:
        model = JournalEntry
        fields = ['entry_type', 'notes', 'photo', 'date']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'})
        }

