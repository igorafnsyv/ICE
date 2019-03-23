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

    #work with quizes!!!!

    components = []
    for module in modules:
        elem = Component.objects.filter(module = module)
        module.components = elem        #stores each component related to that module in module object
    return render(request, "courses/course_detail.html", context = {"course" : course , "modules" : modules, "components": components})

#def manage_module(request, slug):


class ModuleCreate(View):       #class based view to override Post function
   
   #need to identify instructor who created module
   
    def get (self, request, id):
        courseID = Course.objects.get(id = id)
        form = ModuleForm()
        component_form = ComponentForm()
        components = Component.objects.filter(module = None)
        return render (request, 'courses/module_create.html', context = {'form' : form, 'courseID' : courseID, 'comp_form' :component_form, 'components': components})

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
    #need to identify instructor who created component
    def get(self, request, id):
        component_form = ComponentForm()
        components = Component.objects.filter(module = None)    #Should it be then either same Course or no Course?
        module = Module.objects.get(id = id)
        return render(request, 'courses/add_existing_component.html', context = {'form' : component_form, 'module' : module, 'components' : components})
    def post(self, request, id):

        #might result in a case that component is associated with module but not with course
        module = Module.objects.filter(id__iexact = id) #this
        course = module[0].course
        i = 0
        print()
        print()
        print(request.POST.getlist('componentID'))
        print(request.POST.getlist('module'))
        for componentID in request.POST.getlist('componentID'):
            component = Component.objects.get(id__iexact = componentID)
            if request.POST.getlist('module')[i]:
                module = Module.objects.get(id__iexact = request.POST.getlist('module')[i])
                component.module = module
                component.save()
                course = component.module.course
            i += 1
        return redirect(course)

