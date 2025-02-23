from django import forms
from .models import Expence

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expence
        fields = ['expance_name', 'category', 'cost']  
