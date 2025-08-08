from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Transaction, Category


class RegistrationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['date','description','amount','type','category']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

