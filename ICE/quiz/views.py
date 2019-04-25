from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import QuizBank, Question, AnswerOptions

from random import shuffle

from courses.models import Module, Learner, CourseCompletion

from django.views.generic import View

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


# Create your views here.
class QuizAdd(View):

    def get(self, request, id):
        if request.user.is_anonymous:
            redirect('/accounts/login/')
        if not hasattr(request.user, 'instructor'):
            return HttpResponse("<h1>You do not have access to this page</h1>")
        module = Module.objects.get(id__iexact=id)
        quiz_banks = QuizBank.objects.filter(module=None)
        return render(request, 'quiz/add_existing_quiz_bank.html', context={'module': module,
                                                                            'quiz_banks': quiz_banks})

    def post(self, request, id):
        module = Module.objects.get(id__iexact=id)
        course = module.course
        quiz_bank = QuizBank.objects.get(id=request.POST['selected_bank'])
        quiz_bank.module = module
        quiz_bank.save()
        return redirect(course)


class QuizTake(View):

    def get(self, request, quiz_bank_id):
        if request.user.is_anonymous:
            return redirect('/accounts/login')
        if not hasattr(request.user, 'learner'):
            return HttpResponse("<h1>You do not have access to this page</h1>")
        quiz_bank = QuizBank.objects.get(id=quiz_bank_id)
        questions = list(Question.objects.filter(quizBank=quiz_bank))
        shuffle(questions)
        questions = questions[:quiz_bank.required_questions_num]
        for question in questions:
            answer_options = AnswerOptions.objects.filter(question=question)
            question.answer_options = answer_options
        
        return render(request, 'quiz/take_quiz.html', context={'quiz_bank': quiz_bank,
                                                               'questions': questions})

    def post(self, request, quiz_bank_id):
        quiz_bank = QuizBank.objects.get(id=quiz_bank_id)
        pass_rate = quiz_bank.pass_rate
        result = 0
        course_completed = False
        for question, answer in request.POST.items():
            if answer.isdigit():
                answer_result = AnswerOptions.objects.get(id=answer)
                if answer_result.correct_incorrect:
                    result += 1

        if result / quiz_bank.required_questions_num >= pass_rate / 100:

            learner = request.user.learner
            learner.completed_modules.add(quiz_bank.module)

            result_percent = result / quiz_bank.required_questions_num * 100
            course_last_module = Module.objects.filter(course=quiz_bank.course).order_by('-position')[0]
            if course_last_module == quiz_bank.module:

                if len(CourseCompletion.objects.filter(learner=learner)) > 0:
                    # The last course completed credits + CECU for this course
                    cumulative_credits = CourseCompletion.objects.filter(learner=learner).order_by('date_completed')[0].course.credit_units + quiz_bank.course.credit_units
                else:
                    cumulative_credits = quiz_bank.course.credit_units
                # creating CourseCompletion object to store course completion (surprise, surprise)
                CourseCompletion.objects.create(course=quiz_bank.course, learner=learner,
                                                cumulative_credits=cumulative_credits)
                send_email(learner.email,
                           learner.first_name + ' ' + learner.last_name,
                           'Course Completed',
                           'quiz/course_completed_email.html', quiz_bank.course)
                course_completed = True
            learner.save()
            return render(request, "quiz/quiz_result.html", context={'result': result_percent,
                                                                     'course': quiz_bank.course,
                                                                     'course_completed': course_completed})
        fail = True        
        return render(request, "quiz/quiz_result.html", context={'fail': fail,
                                                                 'course': quiz_bank.course})


def send_email(email, name, subject, email_template, course):
    subject, from_email, to = subject, 'admin@ice.com', email
    text_content = ''
    html_content = render_to_string(email_template,
                                    context={'name': name,
                                             'course': course,
                                             'email': email})
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
    return None
