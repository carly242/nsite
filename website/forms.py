from django import forms
from .models import User, Document

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name', 'function','email','email_bureau', 'office_number', 'phone_number', 'city', 'photo','website']
        
    

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['title']


from django.contrib.auth.forms import PasswordResetForm

class CustomPasswordResetForm(PasswordResetForm):
    # Ajoutez des modifications personnalisées au besoin
    pass