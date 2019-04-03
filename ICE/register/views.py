from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect

from django.views.generic import View

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

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
        print(req.json())
        email = req.json()['email']
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
