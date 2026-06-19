from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Application,TransportType
import re

class RegisterForm(UserCreationForm):

    first_name = forms.CharField(max_length=100, required=True, label='ФИО')
    email = forms.EmailField(required=True, label='E-mail')
    phone = forms.CharField(max_length=20, required=True, label='Контактный телефон')
    birth_date = forms.DateField(
        required=True, 
        label='Дата рождения',
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'email', 'password1', 'password2']
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not re.match(r'^[a-zA-Z0-9]{6,}$', username):
            raise forms.ValidationError('Логин должен содержать только латинские буквы и цифры, минимум 6 символов')
        return username

class ApplicationForm(forms.ModelForm):
    
    
    class Meta:
        model = Application
        fields = ['transport_type', 'start_date', 'payment_method']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['transport_type'].queryset = TransportType.objects.all()
        self.fields['transport_type'].empty_label = 'Выберите вид транспорта'

class ReviewForm(forms.Form):
    review = forms.CharField(widget=forms.Textarea(attrs={'rows': 4}), label='Ваш отзыв')