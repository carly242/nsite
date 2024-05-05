from django import forms
from .models import User, Document
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.password_validation import validate_password
from django.utils.translation import gettext as _


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name', 'function','email','email_bureau', 'office_number', 'phone_number', 'city', 'photo','website']
        
    

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['title']


from django.contrib.auth.forms import PasswordResetForm



class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label="Ancien mot de passe", widget=forms.PasswordInput)
    new_password1 = forms.CharField(label="Nouveau mot de passe", widget=forms.PasswordInput)
    new_password2 = forms.CharField(label="Confirmez le nouveau mot de passe", widget=forms.PasswordInput)
    
class CustomSetPasswordForm(SetPasswordForm):
    error_messages = {
        'password_mismatch': _("Les deux mots de passe ne sont pas identiques."),
        'password_too_short': _("Ce mot de passe est trop court! il doit contenir au moins 8 caratères"),
        'password_common': _("Ce mot de passe est trop commun "),
    }

    def clean_new_password1(self):
        password1 = self.cleaned_data.get('new_password1')
        validate_password(password1)  # This will raise a ValidationError if the password is invalid
        return password1

    new_password1 = forms.CharField(label="Nouveau mot de passe", widget=forms.PasswordInput, error_messages={'required': '', 'password_too_short': _("This password is too short. It must contain at least 8 characters."), 'password_common': _("This password is too common.")})
    new_password2 = forms.CharField(label="Confirmez le nouveau mot de passe", widget=forms.PasswordInput, error_messages={'required': '', 'password_mismatch': _("The two password fields didn't match.")})