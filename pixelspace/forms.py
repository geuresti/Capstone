from django import forms

class AccountForm(forms.Form):
    username = forms.CharField(label='username', max_length=100)
    password = forms.CharField(widget=forms.PasswordInput, label='password', max_length=100)
    confirm_password = forms.CharField(widget=forms.PasswordInput, label='retype password', max_length=100)
    email = forms.CharField(label='email', max_length=100)

class UserForm(forms.Form):
    username = forms.CharField(label='username', max_length=100)
    password = forms.CharField(widget=forms.PasswordInput, label='password', max_length=100)

class SettingsForm(forms.Form):
    newPassword = forms.CharField(label='newPassword', max_length=100, required=False)
    retypePassword = forms.CharField(label='retypePassword', max_length=100, required=False)
    deleteAccount = forms.BooleanField(label='deleteAccount', required=False)

class LABForm(forms.Form):
    lightness = forms.FloatField(label='lightness')
    axisA = forms.FloatField(label='axisA')
    axisB = forms.FloatField(label='axisB')

class PixelForm(forms.Form):
    length = forms.IntegerField(label='length')
    width = forms.IntegerField(label='width')
    greyscale = forms.BooleanField(label='greyscale', required=False)
    custom = forms.BooleanField(label='custom', required=False)
    rrangeLow= forms.IntegerField(label='rrangeLow', required=False)
    brangeLow= forms.IntegerField(label='brangeLow', required=False)
    grangeLow= forms.IntegerField(label='grangeLow', required=False)
    rrangeHigh= forms.IntegerField(label='rrangeHigh', required=False)
    brangeHigh= forms.IntegerField(label='brangeHigh', required=False)
    grangeHigh= forms.IntegerField(label='grangeHigh', required=False)

class CustomForm(forms.Form):
    custom = forms.BooleanField(label='custom', required=False)
    rrangeLow= forms.IntegerField(label='rrangeLow', required=False)
    brangeLow= forms.IntegerField(label='brangeLow', required=False)
    grangeLow= forms.IntegerField(label='grangeLow', required=False)
    rrangeHigh= forms.IntegerField(label='rrangeHigh', required=False)
    brangeHigh= forms.IntegerField(label='brangeHigh', required=False)
    grangeHigh= forms.IntegerField(label='grangeHigh', required=False)
class SaveForm(forms.Form):
    png = forms.BooleanField(label='png', required=False)
    jpg = forms.BooleanField(label='jpg', required=False)
    tif = forms.BooleanField(label='tif', required=False)

class MapForm(forms.Form):
    deleteMap = forms.BooleanField(label='deleteMap', required=False)


class confirmDeleteForm(forms.Form):
    confirmDelete = forms.BooleanField(label='confirmDelete', required=False)

class confirmMapDeleteForm(forms.Form):
    confirmMapDelete = forms.BooleanField(label='confirmMapDelete', required=False)
