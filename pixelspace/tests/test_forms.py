
from django.test import TestCase

from pixelspace.forms import UserForm, SettingsForm, CreateAccountForm, LABForm

"""
class AccountForm(forms.Form):
    username = forms.CharField(label='username', max_length=100)
    password = forms.CharField(label='password', max_length=100)
    confirm_password = forms.CharField(label='retype password', max_length=100)
    email = forms.CharField(label='email', max_length=100)

class UserForm(forms.Form):
    username = forms.CharField(label='username', max_length=100)
    password = forms.CharField(label='password', max_length=100)

class SettingsForm(forms.Form):
    newPassword = forms.CharField(label='newPassword', max_length=100, required=False)
    retypePassword = forms.CharField(label='retypePassword', max_length=100, required=False)
    deleteAccount = forms.BooleanField(label='deleteAccount', required=False)

class CreateAccountForm(forms.Form):
    newUser = forms.CharField(label='newUser', max_length=100)
    newPass = forms.CharField(label='newPass', max_length=100)
    confirmPass = forms.CharField(label='newPass', max_length=100)

class LABForm(forms.Form):
    lightness = forms.FloatField(label='lightness')
    axisA = forms.FloatField(label='axisA')
    axisB = forms.FloatField(label='axisB')
"""

class UserForm(TestCase):
    def test_name_form_field_labels(self):
        form = UserForm()
        print("HERE:", form.fields)
        form.fields['username'] = "abcdefg"
        form.fields['password'] = "hijlmno"

        self.assertTrue(
            form.fields['username'].label == "username" and
            form.fields['password'].label == "password"
        )

    def test_form_validity(self):
        form = UserForm()
            #data={'username':'Jane Doe', 'password':'password123'}
        form.fields['username'] = "Jane Doe"
        form.fields['password'] = "password123"
        self.assertTrue(form.is_valid())
