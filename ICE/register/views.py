from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect

from django.views.generic import View

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib.auth.models import User, Group
from courses.models import Learner, Instructor
from django.contrib.auth.forms import UserCreationForm

import requests

from django.http import HttpResponse

class InviteInstructor (View):
    def get(self, request):
        return render(request, template_name='register/invite_instructor.html', context={})

    def post(self, request):
        #return HttpResponse(request.POST['email'])
        email=request.POST['email']
        subject, from_email, to = 'Registration link', 'admin@ice.com', email
        text_content = ''
        html_content = render_to_string('register/signup_email.html',
                                        context={'name': name, 'protocol': 'http', 'domain': 'localhost:8000',
                                                 'email': email})
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()



class SignUp (View):

    def get(self, request):
        if request.user.is_superuser:
            return render(request, template_name='register/invite_instructor.html', context={})
        else:
            return render(request, 'register/signup.html', context={})

    def post(self, request):
        # make the link for registration
        if request.user.is_superuser:
            name = request.POST['first_name'] + ' ' + request.POST['last_name']
            email = request.POST['email']
            Instructor.objects.create(email=email, first_name=request.POST['first_name'], last_name=request.POST['last_name'])
            user_type="instructor"



        if not request.user.is_superuser:
            req = requests.get("https://gibice-hrserver.herokuapp.com/info/" + request.POST['id'])
            if req.text == 'Invalid staff ID':
                return HttpResponse("<h1>Invalid Staff ID</h1>")
            email = req.json()['email']
            Learner.objects.create(first_name=req.json()['first_name'], last_name=req.json()['last_name'],
                                                staff_id=req.json()['id'], email=email)
            name = req.json()['first_name'] + ' ' + req.json()['last_name']
            user_type='learner'
        subject, from_email, to = 'Registration link', 'admin@ice.com', email
        text_content=''
        html_content = render_to_string('register/signup_email.html',
                                        context={'name':name, 'protocol':'http', 'domain':'localhost:8000',
                                                'email':email, 'user_type': user_type})
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        return render(request, 'register/signup_success.html', context={})

class RegisterUser (View):
    def get(self, request, email, type):
        form = UserCreationForm()
        return render(request, 'register/set_login_password.html', context={'email': email, 'form': form,
                                                                            'user_type': type})

    def post(self, request, email, type):
        if int(type) == 1:
            learner = Learner.objects.get(email=email)
            first_name = learner.first_name
            last_name = learner.last_name
            group = Group.objects.get(name='Learners')
            new_user = learner
        if int(type) == 2:
            instructor = Instructor.objects.get(email=email)
            first_name = instructor.first_name
            last_name = instructor.last_name
            group = Group.objects.get(name='Instructors')
            instructor.introduction = request.POST['intro']
            instructor.save()
            new_user = instructor
        form = UserCreationForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.first_name = first_name
            obj.last_name = last_name
            obj.email = email
            obj.save()
            new_user.user = obj
            new_user.save()
            group.user_set.add(obj)
            group.save()


        return render(request, 'register/registration_success.html', context={})