from django import forms
from .models import Account

class AccountForm(forms.Form):
    username = forms.CharField(label='username', max_length=100)
    password = forms.CharField(label='password', max_length=100)
    confirm_password = forms.CharField(label='retype password', max_length=100)
    email = forms.CharField(label='email', max_length=100)

class NameForm(forms.Form):
    username = forms.CharField(label='username', max_length=100)
    password = forms.CharField(label='password', max_length=100)

class createAccForm(forms.Form):
    newUser = forms.CharField(label='newUser', max_length=100)
    newPass = forms.CharField(label='newPass', max_length=100)
    confirmPass = forms.CharField(label='newPass', max_length=100)

class LABForm(forms.Form):
    lightness = forms.FloatField(label='lightness')
    axisA = forms.FloatField(label='axisA')
    axisB = forms.FloatField(label='axisB')

#class AccountForm(forms.ModelForm):
#    class Meta:
#        model = Account
#        fields = ('username', 'password', 'confirm password')
