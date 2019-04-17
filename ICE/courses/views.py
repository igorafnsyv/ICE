from django.shortcuts import render, redirect
from .models import Course, Module, Component, Learner, Instructor, Category, CourseCompletion
from django.contrib.auth.models import Group, User
from quiz.models import QuizBank
from django.http import HttpResponse

from django.views.generic import View

from .forms import ModuleForm, ComponentForm, CourseForm
# Create your views here.


# since it is landing page, verify user type, depending on this, redirect users
# admin to admin and others to the func
def courses_list(request):
    if request.user.is_anonymous:
        return redirect('/accounts/login/')
    if request.user.is_superuser:
        return render(request, 'courses/admin_start_page.html', context={})

    if str(request.user.groups.all()[0]) == 'Instructors':
        # has to return all courses that were created by this particular Instructor
        courses = Course.objects.filter(instructor=request.user.instructor)
        return render(request, 'courses/courses_list.html', context={'courses': courses})
    else:
        courses = Learner.objects.get(staff_id=request.user.learner.staff_id).courses.all()
        return render(request, 'courses/learner_course_list.html', context={'courses': courses})


def completed_courses_list(request):
    if request.user.is_anonymous:
        return redirect('/accounts/login')
    completion_records = CourseCompletion.objects.filter(learner=request.user.learner)
    total_credits = 0
    for completion in completion_records:
        total_credits += completion.course.credit_units
    return render(request, 'courses/completed_courses_list.html', context={'completion_records': completion_records,
                                                                           'total_credits': total_credits})


# returns all courses available for enrollment
def all_courses(request):
    if request.user.is_anonymous:
        return redirect('/accounts/login')
    this_learner = request.user.learner
    courses_can_enroll = Course.objects.filter(status=1).exclude(learner=this_learner)
    categories = Category.objects.all()
    selected_category = ''

    # if user has selected category, extract it and show courses from that category
    if request.GET and request.GET['category']:
        selected_category = Category.objects.get(title=request.GET['category'])
        courses_can_enroll = courses_can_enroll.filter(category=selected_category)

    return render(request, 'courses/courses_for_enrollment.html', context={'courses': courses_can_enroll,
                                                                           'categories': categories,
                                                                           'selected_category': selected_category})


def course_enroll(request, course_id):

    # todo where to redirect user after successful enrollment?
    # todo fix redirection to course
    # To the list of courses learner enrolled or continue enrollment?
    if request.user.is_anonymous:
        return redirect('/accounts/login')
    this_learner = request.user.learner
    course = Course.objects.get(id=course_id)
    this_learner.courses.add(course)
    this_learner.save()
    return redirect('course_list_url')


def study_course(request, course_id):
    # todo merge with course detail
    if request.user.is_anonymous:
        return redirect('/accounts/login')
    course = Course.objects.get(id__iexact=course_id)
    modules = Module.objects.filter(course=course)
    print(modules)
    availability = True
    learner = request.user.learner
    completed_modules = learner.completed_modules.all()
    for module in modules:
        if module in completed_modules:
            module.available = True
        else:
            module.available = availability
            availability = False
        
    return render(request, "courses/study_course.html", context={'course': course,
                                                                 'modules': modules,
                                                                 'learner': learner})


def study_module(request, id):
    if request.user.is_anonymous:
        return redirect('/accounts/login')
    module = Module.objects.get(id__iexact=id)
    components = Component.objects.filter(module=module).order_by('position')
    quiz_bank = QuizBank.objects.get(module=module)

    quiz_taken = module in request.user.learner.completed_modules.all()
    return render(request, 'courses/study_module.html', context={'module': module,
                                                                 'components': components,
                                                                 'quiz_bank': quiz_bank,
                                                                 'quiz_taken': quiz_taken})


# shows details of the particular course
def course_detail(request, id):
    if request.user.is_anonymous:
        return redirect('/accounts/login')
    course = Course.objects.get(id__iexact=id)
    modules = Module.objects.filter(course=course).order_by('position')
    components = []
    for module in modules:
        elem = Component.objects.filter(module=module).order_by('position')

        # stores each component related to that module in module object
        module.components = elem
        quiz_bank = QuizBank.objects.filter(module=module)[:1]
        module.quiz_bank = quiz_bank
        
    return render(request, 'courses/course_detail.html', context={'course': course,
                                                                  'modules': modules,
                                                                  'components': components})


class CourseCreate(View):
    def get(self, request):
        if request.user.is_anonymous:
            return redirect('/accounts/login')
        form = CourseForm()
        instructor = request.user.instructor
        return render(request, 'courses/course_create.html', context={'form': form,
                                                                      'instructor': instructor})

    # todo identify instructor by id rather than name and surname
    def post (self, request):
        bound_course = CourseForm(request.POST)
        instructor = Instructor.objects.get(first_name=request.POST['instructor_first_name'],
                                            last_name=request.POST['instructor_last_name'])
        if bound_course.is_valid:
            obj = bound_course.save(commit=False)
            obj.instructor = instructor
            obj.save()
        courses = Course.objects.all()
        return redirect(courses[len(courses) - 1])


# todo merge with component delete
def module_delete(request, module_id):
    if request.user.is_anonymous:
        return redirect('/accounts/login')
    module = Module.objects.get(id__iexact=module_id)
    course = module.course
    removed_position = module.position
    all_modules = Module.objects.filter(course=course)
    for current_module in all_modules:
        if current_module.position > removed_position:
            current_module.position -= 1
            current_module.save()
    module.delete()
    return redirect(course)


def component_delete(request, component_id):
    if request.user.is_anonymous:
        return redirect('/accounts/login')
    component = Component.objects.get(id__iexact=component_id)
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


def component_remove_module(request, component_id):
    if request.user.is_anonymous:
        return redirect('/accounts/login')
    component = Component.objects.get(id=component_id)
    component.module = None
    component.save()
    return redirect(component.course)
# class based view to override Post function


class ModuleCreate (View):

    def get(self, request, course_id):
        if request.user.is_anonymous:
            return redirect('/accounts/login/')
        course = Course.objects.get(id=course_id)
        form = ModuleForm()
        component_form = ComponentForm()
        components = Component.objects.filter(course=course, module=None)
        quiz_banks = QuizBank.objects.filter(course=course, module=None)
        return render(request, 'courses/module_create.html', context={'form': form,
                                                                      'course': course,
                                                                      'comp_form': component_form,
                                                                      'components': components,
                                                                      'quiz_banks': quiz_banks})

    def post(self, request, course_id):
        instructor = request.user.instructor
        course = Course.objects.get(id__iexact=course_id)
        bound_module = ModuleForm(request.POST)
        if bound_module.is_valid():
            obj = bound_module.save(commit=False)
            obj.course = course
            obj.instructor = instructor

            # if Position is not specified by tutor
            if 'position' not in request.POST:

                # get total number of positions
                position = Module.objects.filter(course=course).count()

                # position = append to the ends
                obj.position = position + 1
            obj.save()
            new_module = Module.objects.get(id=obj.id)
            component_position = 1
            for key, value in request.POST.items():
                if "component" in key:
                    component = Component.objects.get(id__iexact=value)
                    component.module = new_module
                    component.position = component_position
                    component_position += 1
                    component.save()
                if 'quiz' in key:
                    quiz_bank = QuizBank.objects.get(id__iexact=value)
                    quiz_bank.module = new_module
                    quiz_bank.save()
            return redirect(course)
              

class ComponentCreate(View):

    # todo identify instructor who created component
    def get(self, request, module_id):
        if request.user.is_anonymous:
            return redirect('/accounts/login/')
        component_form = ComponentForm()
        module = Module.objects.get(id=module_id)
        course = module.course
        components = Component.objects.filter(course=course, module=None)
        return render(request, 'courses/add_existing_component.html', context={'form': component_form,
                                                                               'module': module,
                                                                               'components': components})

    def post(self, request, module_id):
        # might result in a case that component is associated with module but not with course
        module = Module.objects.get(id__iexact=module_id)
        course = module.course

        # traverse dictionary as key value pair
        for key, componentID in request.POST.items():

            # if string 'component' is found in key
            if "component" in key:
                component = Component.objects.get(id__iexact=componentID)
                component.module = module
                current_position = 1
                previous_components = Component.objects.filter(module=module).order_by('-position')
                if len(previous_components) > 1:
                    current_position = previous_components[0].position + 1
                component.position = current_position
                component.save()
        return redirect(course)

