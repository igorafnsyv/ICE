from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect

from django.views.generic import View

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib.auth.models import User, Group
from courses.models import Learner
from django.contrib.auth.forms import UserCreationForm

import requests

from django.http import HttpResponse

class SignUp(View):

    def get(self, request):
        return render(request, 'register/signup.html', context={})

    def post(self, request):
        # make the link for registration
        req = requests.get("https://gibice-hrserver.herokuapp.com/info/" + request.POST['id'])
        if req.text == 'Invalid staff ID':
            return HttpResponse("<h1>Invalid Staff ID</h1>")
        email = req.json()['email']
        # create a basic user information now. Set user to Learners group
        #new_user = User.objects.create(first_name=req.json()['first_name'], last_name=req.json()['last_name'],
        #                              email=email)
        #group = Group.objects.get(name='Learners')
        #group.user_set.add(new_user)
        #group.save()
        Learner.objects.create(first_name=req.json()['first_name'], last_name=req.json()['last_name'],
                                            staff_id=req.json()['id'], email=email)
        name = req.json()['first_name'] + ' ' + req.json()['last_name']
        subject, from_email, to = 'Registration link', 'admin@ice.com', email
        text_content=''
        html_content = render_to_string('register/signup_email.html',
                                        context = {'name' : name, 'protocol' : 'http', 'domain' : 'localhost:8000',
                                                                                 'email' : email})
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        return render(request, 'register/signup_success.html', context={})

class RegisterUser(View):

    def get(self, request, email):
        form = UserCreationForm()
        return render(request, 'register/set_login_password.html', context={'email':email, 'form': form})

    def post(self, request, email):
        learner = Learner.objects.get(email=email)
        form = UserCreationForm(request.POST)
        dir(form)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.first_name = learner.first_name
            obj.last_name = learner.last_name
            obj.email = email
            obj.save()
            learner.user = obj
            learner.save()
            group = Group.objects.get(name='Learners')
            group.user_set.add(obj)
            group.save()
        return HttpResponse("<h1>Hey!</h1>")