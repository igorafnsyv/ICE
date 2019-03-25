from django.shortcuts import render, redirect
from .models import Course, Module, Component, Learner
from quiz.models import QuizBank
from django.http import HttpResponse

from django.views.generic import View

from .forms import ModuleForm, ComponentForm
# Create your views here.

def courses_list(request):
    #has to return all courses that were created by this paticular Instructor
    courses = Course.objects.filter(instructor = "Dutch Van Der Linde") #assume this is default tutor now. How to get the name of the logged in tutor?
    return render(request, "courses/courses_list.html", context = {'courses' : courses})


def learner_course_list(request):   #mege it later with course_list
    courses = Learner.objects.filter(staff_id = 1)[0].courses.all()          #later filter to actual staff_id
    return render(request, "courses/learner_course_list.html", context = {'courses' : courses})

def study_course(request, id):      #merge it later with course_detail
    course = Course.objects.get(id__iexact = id)
    modules = Module.objects.filter(course = course)
    print(modules)
    availability = True
    learner = Learner.objects.filter(staff_id = 1)
    completed_modules = learner[0].completed_modules.all()
    for module in modules:
        if module in completed_modules:
            module.available = True
        else :
            module.available = availability
            availability = False
        
    return render(request, "courses/study_course.html", context = {"course": course, "modules" : modules, "learner" : learner})

def study_module(request, id):
    module = Module.objects.get(id__iexact = id)
    components = Component.objects.filter(module = module).order_by('position')
    quiz_bank = QuizBank.objects.get(module = module)
    return render (request, 'courses/study_module.html', context = {'module' : module, 'components' : components, 'quiz_bank' : quiz_bank})


def course_detail(request, slug):   #shows details of the particular course
    course = Course.objects.get(slug__iexact = slug)
    modules = Module.objects.filter(course = course).order_by('position')
    components = []
    for module in modules:
        elem = Component.objects.filter(module = module).order_by('position')
        module.components = elem        #stores each component related to that module in module object
        quiz_bank = QuizBank.objects.filter(module = module)[:1]
        module.quiz_bank = quiz_bank
        
    return render(request, "courses/course_detail.html", context = {"course" : course , "modules" : modules, "components": components})



class ModuleCreate(View):       #class based view to override Post function
   
   #need to identify instructor who created module
   
    def get (self, request, id):
        courseID = Course.objects.get(id = id)
        form = ModuleForm()
        component_form = ComponentForm()
        components = Component.objects.filter(module = None)
        return render (request, 'courses/module_create.html', context = {'form' : form, 'courseID' : courseID, 'comp_form' :component_form, 'components': components})

    def post(self, request, id):
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
        module = Module.objects.filter(id__iexact = id) 
        course = module[0].course
        i = 0
        for componentID in request.POST.getlist('componentID'):
            component = Component.objects.get(id__iexact = componentID)
            if request.POST.getlist('module')[i]:
                module = Module.objects.get(id__iexact = request.POST.getlist('module')[i])
                component.module = module
                current_position = 0
                previous_components = Component.objects.filter(module = module).order_by('-position')
                if len(previous_components) > 0:
                    current_position = previous_components[0].position + 1

                component.position = current_position
                component.save()
                course = component.module.course
            i += 1
        return redirect(course)




