from django import forms

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

class PixelForm(forms.Form):
    length = forms.IntegerField(label='length')
    width = forms.IntegerField(label='width')
    greyscale = forms.BooleanField(label='greyscale', required=False)

class SaveForm(forms.Form):
    png = forms.BooleanField(label='png', required=False)
    jpg = forms.BooleanField(label='jpg', required=False)
    tif = forms.BooleanField(label='tif', required=False)

class confirmDeleteForm(forms.Form):
    confirmDelete = forms.BooleanField(label='confirmDelete', required=False)
