from django import forms
from django.forms.widgets import TextInput

security_question_first_options = [
    ('Q1', 'What is the name of your first pet?'),
    ('Q2', 'What is your favorite ice cream flavor?'),
    ('Q3', 'What was your favorite stuffed animal?'),
]

security_question_second_options = [
    ('Q4', 'What is your favorite sports team?'),
    ('Q5', 'What is the name of your high school?'),
    ('Q6', 'What is the name of your favorite teacher?'),
]

class AccountForm(forms.Form):
    username = forms.CharField(label='username', max_length=100)
    password = forms.CharField(widget=forms.PasswordInput, label='password', max_length=100)
    confirm_password = forms.CharField(widget=forms.PasswordInput, label='retype password', max_length=100)
    email = forms.CharField(label='email', max_length=100)

    question_one = forms.CharField(
        label='Question One',
        widget=forms.Select(choices=security_question_first_options)
    )

    answer_one = forms.CharField(label='Answer One', max_length=100)

    question_two = forms.CharField(
        label='Question Two',
        widget=forms.Select(choices=security_question_second_options)
    )

    answer_two = forms.CharField(label='Answer Two', max_length=100)

class SecurityQuestionsForm(forms.Form):
    username = forms.CharField(label='Username', required=False, max_length=100)
    answer_one = forms.CharField(label='Answer One', required=False, max_length=100)
    answer_two = forms.CharField(label='Answer Two', required=False, max_length=100)

class UserForm(forms.Form):
    username = forms.CharField(label='username', max_length=100)
    password = forms.CharField(widget=forms.PasswordInput, label='password', max_length=100)

class SettingsForm(forms.Form):
    # added required=False
    newPassword = forms.CharField(widget=forms.PasswordInput, label='newPassword', max_length=100, required=False)
    retypePassword = forms.CharField(widget=forms.PasswordInput, label='retypePassword', max_length=100, required=False)

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
    submitMap = forms.BooleanField(label='submitMap', required=False)

class commentForm(forms.Form):
    content = forms.CharField(label='content')

class LikeForm(forms.Form):
    IDofMap = forms.IntegerField(widget=forms.HiddenInput())
    commentAuthor = forms.CharField(widget=forms.HiddenInput())
    dataURL = forms.CharField(widget=forms.HiddenInput())

class confirmDeleteForm(forms.Form):
    confirmDelete = forms.BooleanField(label='confirmDelete', required=False)

class confirmMapDeleteForm(forms.Form):
    confirmMapDelete = forms.BooleanField(label='confirmMapDelete', required=False)

class ShapeForm(forms.Form):
    shape = forms.ChoiceField(choices = (("rectangle","rectangle"),("oval","oval"),("polygon","polygon")))

# CHANGES
class RectangleForm(forms.Form):
    logoLen = forms.IntegerField(label='logoLen')
    logoWid = forms.IntegerField(label='logoWid')
    color = forms.CharField(label='color', max_length=100)

    text = textColor = forms.CharField(label='text', max_length=100)
    textColor = forms.CharField(label='textColor', max_length=100)
    shape = forms.CharField(widget=forms.HiddenInput())

class OvalForm(forms.Form):
    ovalLen = forms.IntegerField(label='ovalLen')
    ovalWid = forms.IntegerField(label='ovalWid')
    color = forms.CharField(label='color', max_length=100)
    text = textColor = forms.CharField(label='text', max_length=100)
    textColor = forms.CharField(label='textColor', max_length=100)
    shape = forms.CharField(widget=forms.HiddenInput())

class PolyForm(forms.Form):
    polySize = forms.IntegerField(label='polySize')
    noSides = forms.IntegerField(label='noSides')
    color = forms.CharField(label='color', max_length=100)
    text = textColor = forms.CharField(label='text', max_length=100)
    textColor = forms.CharField(label='textColor', max_length=100)
    shape = forms.CharField(widget=forms.HiddenInput())

class saveLogo(forms.Form):
    logoLen = forms.IntegerField(widget=forms.HiddenInput())
    logoWid = forms.IntegerField(widget=forms.HiddenInput())
    polySize = forms.IntegerField(widget=forms.HiddenInput())
    noSides = forms.IntegerField(widget=forms.HiddenInput())
    ovalLen = forms.IntegerField(widget=forms.HiddenInput())
    ovalWid = forms.IntegerField(widget=forms.HiddenInput())
    color = forms.CharField(widget=forms.HiddenInput())
    text = textColor = forms.CharField(widget=forms.HiddenInput())
    textColor = forms.CharField(widget=forms.HiddenInput())
    shape = forms.CharField(widget=forms.HiddenInput())
    logo = forms.CharField(widget=forms.HiddenInput())
