from django.shortcuts import render, redirect
from .models import Course, Module, Component
from django.http import HttpResponse

from django.views.generic import View

from .forms import ModuleForm, ComponentForm
# Create your views here.

def courses_list(request):
    #has to return all courses that were created by this paticular Instructor
    courses = Course.objects.filter(instructor = "Dutch Van Der Linde") #assume this is default tutor now. How to get the name of the logged in tutor?
    return render(request, "courses/courses_list.html", context = {'courses' : courses})

def course_detail(request, slug):   #shows details of the particular course
    course = Course.objects.get(slug__iexact = slug)
    modules = Module.objects.filter(course = course).order_by('position')
    #component = Component.objects.get(title = "First Component") #check this
    components = []
    for module in modules:
        elem = Component.objects.filter(module = module)
        module.components = elem        #stores each component related to that module in module object
    return render(request, "courses/course_detail.html", context = {"course" : course , "modules" : modules, "components": components})

#def manage_module(request, slug):


class ModuleCreate(View):       #class based view to override Post function
    def get (self, request, id):
        courseID = Course.objects.get(id = id)
        form = ModuleForm()
        return render (request, 'courses/module_create.html', context = {'form' : form, 'courseID' : courseID})

    def post(self, request, id): #update to track position of insertion

        course = Course.objects.get(title__iexact = id)
        bound_module = ModuleForm(request.POST)

  
        if bound_module.is_valid():
            obj = bound_module.save(commit = False)
            obj.course = course
            if 'position' not in request.POST:  #if Position is not specified by tutor
                position = Module.objects.filter(course = course).count() #get total number of positions
                obj.position = position + 1 #position = append to the ends
            obj.save()
            return redirect(course)
              

class ComponentCreate(View):
    #def get #should be used to create an interface for component creation
    def post(self, request, id):
        module = Module.objects.filter(title__iexact = id)
        course = module[0].course
        component = Component.objects.create(title = 'Freshly added component', body = 'There is some text. Trust me, I am an Engineer', module = module[0])
        component_image = Component.objects.create(title = 'Image of Component', image = '/images/blame.jpg', module = module[0])
        return redirect(course)

