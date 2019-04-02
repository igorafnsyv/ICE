from django.shortcuts import render, redirect
from .models import Course, Module, Component, Learner, Instructor
from quiz.models import QuizBank
from django.http import HttpResponse

from django.views.generic import View

from .forms import ModuleForm, ComponentForm, CourseForm
# Create your views here.

def courses_list(request):
    # has to return all courses that were created by this particular Instructor
    courses = Course.objects.filter(instructor = "Dutch van der Linde") # assume this is default tutor now. How to get the name of the logged in tutor?
    return render(request, "courses/courses_list.html", context = {'courses' : courses})


def learner_course_list(request):   # mege it later with course_list
    courses = Learner.objects.filter(staff_id = 1)[0].courses.all()          # later filter to actual staff_id
    return render(request, "courses/learner_course_list.html", context = {'courses' : courses})



def study_course(request, id):      # merge it later with course_detail
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
    quiz_taken = module in Learner.objects.get(staff_id = 1).completed_modules.all()    #change to proper staff id. Checks whether Learner completed this module
    return render (request, 'courses/study_module.html', context = {'module' : module, 'components' : components, 'quiz_bank' : quiz_bank, 'quiz_taken' : quiz_taken})


def course_detail(request, id):   #shows details of the particular course
    course = Course.objects.get(id__iexact = id)
    modules = Module.objects.filter(course = course).order_by('position')
    components = []
    for module in modules:
        elem = Component.objects.filter(module = module).order_by('position')
        module.components = elem        #stores each component related to that module in module object
        quiz_bank = QuizBank.objects.filter(module = module)[:1]
        module.quiz_bank = quiz_bank
        
    return render(request, "courses/course_detail.html", context = {"course" : course , "modules" : modules, "components": components})


class CourseCreate(View):
    def get(self, request):
        form = CourseForm()
        instructor = "Dutch van der Linde"
        return render (request, 'courses/course_create.html', context = {'form' : form, 'instructor' : instructor})

    def post (self, request):
        bound_course = CourseForm(request.POST)
        
        instructor = request.POST['instructor']
        if bound_course.is_valid:
            obj = bound_course.save(commit = False)
            obj.instructor = instructor
            obj.save()
        courses = Course.objects.all()
        return redirect(courses[len(courses) - 1])

def module_delete(request, id):
    module = Module.objects.get(id__iexact = id)
    course = module.course
    removed_position = module.position
    all_modules = Module.objects.filter(course=course)
    for current_module in all_modules:
        if current_module.position > removed_position:
            current_module.position -= 1
            current_module.save()
    module.delete()
    return redirect (course)

def component_delete(request, id):
    component = Component.objects.get(id__iexact=id)
    module = component.module
    course = module.course
    removed_position = component.position
    all_components = Component.objects.filter(module=module)
    for current_component in all_components:
        if current_component.position > removed_position:
            current_component.position -= 1
            current_component.save()
    component.delete()
    return redirect(course)

class ModuleCreate(View):       #class based view to override Post function
   
   #need to identify instructor who created module
   
    def get (self, request, id):
        course = Course.objects.get(id = id)
        form = ModuleForm()
        component_form = ComponentForm()
        components = Component.objects.filter(course = course, module = None)
        quiz_banks = QuizBank.objects.filter(course = course, module = None)
        return render (request, 'courses/module_create.html', context = {'form' : form, 'course' : course, 'comp_form' :component_form, 'components': components, 'quiz_banks' : quiz_banks})

    def post(self, request, id):
        course = Course.objects.get(id__iexact = id)
        bound_module = ModuleForm(request.POST)
        instructor = Instructor.objects.get(name__iexact = "Dutch van der Linde")       #proper identification later
        if bound_module.is_valid():
            obj = bound_module.save(commit = False)
            obj.course = course
            obj.instructor = instructor                    
            if 'position' not in request.POST:  #if Position is not specified by tutor
                position = Module.objects.filter(course = course).count() #get total number of positions
                obj.position = position + 1 #position = append to the ends
            obj.save()
            new_module = Module.objects.get(id = obj.id)
            component_position = 1
            for key, value in request.POST.items():
                if "component" in key:
                    component = Component.objects.get(id__iexact = value)
                    component.module = new_module
                    component.position = component_position
                    component_position += 1
                    component.save()
                if 'quiz' in key:
                    quiz_bank = QuizBank.objects.get(id__iexact = value)
                    quiz_bank.module = new_module
                    quiz_bank.save()
            return redirect(course)
              

class ComponentCreate(View):
    #def get #should be used to create an interface for component creation
    #need to identify instructor who created component
    def get(self, request, id):
        component_form = ComponentForm()
        module = Module.objects.get(id = id)
        course = module.course
        components = Component.objects.filter(course = course, module = None)    #Should it be then either same Course or no Course?
        return render(request, 'courses/add_existing_component.html', context = {'form' : component_form, 'module' : module, 'components' : components})
    def post(self, request, id):

        #might result in a case that component is associated with module but not with course
        module = Module.objects.get(id__iexact = id) 
        course = module.course
        for key, componentID in request.POST.items():
            if "component" in key:
                component = Component.objects.get(id__iexact = componentID)
                component.module = module
                current_position = 1
                previous_components = Component.objects.filter(module = module).order_by('-position')
                if len(previous_components) > 1:
                    current_position = previous_components[0].position + 1
                component.position = current_position
                component.save()
        return redirect(course)