from django import forms
from .models import ContactForm, Login, AdminLogin, Editpage


class FormContactForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = ContactForm
        fields = ["username", "firstname", "lastname", "dob", "gender",
                  "email", "contact", "address", "password", "salary"]
        labels = {"username": "Username", "firstname": 'First Name',
                  "lastname": 'Last Name', "dob": 'DOB(y-m-d)',
                  "gender": 'Gender   ',
                  "email": 'Email', "contact": 'Number',
                  "address": 'Address', "password": "Password", "salary": "Monthly Salary"}


class FormLoginForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Login
        fields = ["username", "password"]
        labels = {"username": "Username", "password": "Password"}


class FormAdminForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = AdminLogin
        fields = ["username", "password"]
        labels = {"username": "Username", "password": "Password"}


class FormEditForm(forms.ModelForm):
    class Meta:
        model = Editpage
        fields = ["primary_key", "updated_field", "updated_value"]
        labels = {"primary_key": 'id', "updated_field":'updated_field', "updated_value":'updated_value'}
