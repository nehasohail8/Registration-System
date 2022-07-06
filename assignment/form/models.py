from django.core.validators import MinLengthValidator, RegexValidator
from django.db import models

GENDER_CHOICES = (
    ('male', 'MALE'),
    ('female', 'FEMALE'),
    ('other', 'OTHER')
)
alphanumeric = RegexValidator(
    r'^[a-zA-Z0-9]([._-](?![._-])|[a-zA-Z0-9]){3,18}[a-zA-Z0-9]$',
    'Only alphanumeric characters are allowed.')
alphabets = RegexValidator(r'^[A-Za-z]+$', 'only alphabets are allowed')
numbers = RegexValidator(r'^[0-9]+$', 'only numbers are allowed')
contact_number = RegexValidator(r'^[0-9]{11}$',
                                'only positive 11 digits are allowed')


class ContactForm(models.Model):
    username = models.CharField(max_length=100, validators=[alphanumeric])
    firstname = models.CharField(max_length=45, validators=[alphabets])
    lastname = models.CharField(max_length=45, validators=[alphabets])
    dob = models.DateField()
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES)
    email = models.EmailField(max_length=254, unique=True)
    contact = models.CharField(max_length=11, validators=[contact_number])
    salary = models.BigIntegerField(validators=[numbers])
    address = models.CharField(max_length=100, validators=[
        MinLengthValidator(10, 'must contain atleast 10 characters')])
    password = models.CharField(max_length=50)


class Login(models.Model):
    username = models.CharField(max_length=100, validators=[alphanumeric])
    password = models.CharField(max_length=50)


class AdminLogin(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=50)


class Editpage(models.Model):
    primary_key = models.IntegerField()
    updated_field = models.CharField(max_length=2000)
    updated_value = models.CharField(max_length=2000)
