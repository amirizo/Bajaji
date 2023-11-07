from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Receiver 

from django.contrib.auth.forms import AuthenticationForm
from django.forms.widgets import PasswordInput, TextInput

#Register/create USer

class CreateUserform(UserCreationForm):
    phone_number = forms.CharField(max_length=15, required=True, help_text="Required. Enter your phone number.")
    class Meta:
        model = User
        fields = ['username', 'email','phone_number', 'password1', 'password2']

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput())
    password = forms.CharField(widget=PasswordInput())


class MyfileUploadForm(forms.Form):
    files = forms.FileField(widget=forms.FileInput(attrs={'class': 'form-control'}))


class PaymentForm(forms.Form):
    name = forms.CharField(max_length=200, required=True, label="Driver Name....")
    phone = forms.CharField(max_length=15, required=True, label="Phone Number....")
    phone11 = forms.CharField(max_length=15, required=True, label="Payment Number....")


class WithDrawForm(forms.Form):
    amount_to_withdraw =  forms.DecimalField(
        label='Amount to Withdraw',
        min_value=0,
        widget=forms.NumberInput(attrs={'step': '0.01'})
    )

