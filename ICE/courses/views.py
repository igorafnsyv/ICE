from django.shortcuts import render, redirect
from .models import Course, Module, Component
from django.http import HttpResponse

from django.views.generic import View

from .forms import ModuleForm
# Create your views here.

def courses_list(request):
    #has to return all courses that were created by this Instructor
    courses = Course.objects.filter(instructor = "Dutch Van Der Linde") #assume this is default tutor now. How to get the name of the logged in tutor?
    return render(request, "courses/courses_list.html", context = {'courses' : courses})

def course_detail(request, slug):
    course = Course.objects.get(slug__iexact = slug)
    modules = Module.objects.filter(course = course).order_by('position')
    return render(request, "courses/course_detail.html", context = {"course" : course , "modules" : modules})

#def manage_module(request, slug):


class ModuleCreate(View):
    def get (self, request, id):
        courseID = Course.objects.get(id = id)
        form = ModuleForm()
        return render (request, 'courses/module_create.html', context = {'form' : form, 'courseID' : courseID})

    def post(self, request, id):

        course = Course.objects.get(title__iexact = id)
        bound_module = ModuleForm(request.POST)

  
        if bound_module.is_valid():
            obj = bound_module.save(commit = False)
            obj.course = course
            if 'position' not in request.POST:
                position = Module.objects.filter(course = course).count()
                obj.position = position + 1 #if not specified explicitly
            obj.save()
            return redirect(course)
              