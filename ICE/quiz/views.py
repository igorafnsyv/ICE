from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def quiz_list(request):
    return HttpResponse("<h1>I am here</h1>")