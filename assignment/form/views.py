import requests
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template.loader import render_to_string
from django.views.decorators.http import require_http_methods

from .forms import FormContactForm, FormLoginForm, FormAdminForm, FormEditForm
from .models import *
from django.shortcuts import render
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.views.generic import View
from .process import html_to_pdf

OLD_USER = ''


def showall(request):
    message=''
    if request.method == "POST":
        data_list = ContactForm.objects.all()
        form = FormEditForm(request.POST)
        if form.is_valid():
            data_list = ContactForm.objects.all()
            key=form.cleaned_data.get('primary_key')
            field=str(form.cleaned_data.get('updated_field'))
            value=form.cleaned_data.get('updated_value')

            for items in data_list:
                if items.id == key:
                    setattr(items, field, value )
                    try:
                        items.save()
                    except:
                        message='invalid input'

        return render(request, 'form/submitted.html',
                          context={'data_list': data_list, 'username': 'Admin',
                                   'title': 'All Data Information', 'href': '',
                                   'form': FormEditForm(), 'message':message})
    else:
        data = ContactForm.objects.all()
        form = FormEditForm()
        return render(request, 'form/submitted.html',
                      context={'data_list': data, 'username': 'Admin',
                               'title': 'All Data Information', 'href': '',
                               'form': form, 'message': message})


def editform(request, user_id):
    global OLD_USER
    band = ContactForm.objects.get(id=user_id)
    if request.method == "POST":
        form = FormContactForm(request.POST, instance=band)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            if username != OLD_USER:
                message = f'oop! {OLD_USER} You cannot change your username'
                return render(request, 'form/logged.html',
                              {'form': form, 'message': message})
            form.save()
            return formdisplay(request, band.username)

    else:
        form = FormContactForm(instance=band)
        OLD_USER = band.username
    return render(request, 'form/logged.html', {'form': form, 'message': ''})


def formdisplay(request, username):
    data_list = ContactForm.objects.all()
    if username != '':
        new_dict = {}
        for item in data_list:
            if item.username == username:
                new_dict = {item}
                context = {'data_list': new_dict, 'username': item.username,
                           'title': 'My Account Information',
                           'href': f'http://127.0.0.1:8000/Edit/{item.id}'}
                break
    else:
        context = {'data_list': data_list, 'username': '',
                   'title': 'All Data Information', 'href': ''}
    return render(request, 'form/formdisplay.html', context)


def showform(request):
    message = ''
    if request.method == "POST":
        form = FormContactForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            for item in ContactForm.objects.all():
                if item.username == username:
                    message = 'oop! Looks like you are already registered!'
                    return render(request, 'form/contactform.html',
                                  {'form': form, 'message': message})
            form.save()
            # subject = f'Hello {username} ! Your account has been successfully registered.'
            # email = EmailMessage('Registration Successful', subject, to=[email])
            # email.send()
            return formdisplay(request, username)
    else:
        form = FormContactForm()
    return render(request, 'form/contactform.html',
                  {'form': form, 'message': message})


def showlogin(request):
    if request.method == "POST":
        form = FormLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            for item in ContactForm.objects.all():
                if item.username == username and item.password == password:
                    return formdisplay(request, username)

            message = 'Oops! Either your username or password is incorrect'
            return render(request, 'form/loginform.html',
                          {'form': form, 'message': message})
    else:
        form = FormLoginForm()
    return render(request, 'form/loginform.html', {'form': form})


def showAdmin(request):
    if request.method == "POST":
        form = FormAdminForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            if username == 'admin' and password == '123':
                return HttpResponseRedirect('admindisplay')

            message = 'Oops! Either your username or password is incorrect'
            return render(request, 'form/admin.html',
                          {'form': form, 'message': message})
    else:
        form = FormAdminForm()
    return render(request, 'form/admin.html', {'form': form})


# Creating a class based view
class GeneratePdf(View):
    def get(self, request, *args, **kwargs):
        data_list = ContactForm.objects.all()
        open('C:/Users/DELL/assignment/form/templates/form/template.html',
             "w").write(
            render_to_string('form/pdf.html', context={'data_list': data_list}))
        # getting the template
        pdf = html_to_pdf('form/template.html')

        # rendering the template
        return HttpResponse(pdf, content_type='application/pdf')


def graph(request):
    gender_list = [['female', 0], ['male', 0], ['other', 0]]
    salary_lst = [['number', 'salary']]
    salary_dict = {}
    data_list = ContactForm.objects.all()
    for item in data_list:
        if item.gender == 'female':
            gender_list[0][1] += 1
        elif item.gender == 'male':
            gender_list[1][1] += 1
        else:
            gender_list[2][1] += 1
    for item in data_list:
        if item.salary not in salary_dict:
            salary_dict[item.salary] = 0
        salary_dict[item.salary] += 1
    for key, val in salary_dict.items():
        salary_lst.append([val, key])
    return render(request, 'form/graphs.html',
                  {'gender_list': gender_list, 'salary_list': salary_lst})
