from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import QuizBank, Question, AnswerOptions

from random import shuffle

from courses.models import Module, Learner, CourseCompletion

from .forms import QuizForm

from django.views.generic import View


# Create your views here.
class QuizAdd(View):

    def get(self, request, id):
        if request.user.is_anonymous:
            redirect('/accounts/login/')
        module = Module.objects.get(id__iexact=id)
        quiz_banks = QuizBank.objects.filter(module=None)
        quiz_bank_form = QuizForm()
        return render (request, 'quiz/add_existing_quiz_bank.html', context={'module': module,
                                                                             'quiz_banks': quiz_banks,
                                                                             'form': quiz_bank_form})

    def post(self, request, id):
        module = Module.objects.filter(id__iexact = id)
        i = 0
        course = module[0].course
        for quiz_bank_id in request.POST.getlist('quiz_bank_id'):
            quiz_bank = QuizBank.objects.get(id__iexact=quiz_bank_id)
            if request.POST.getlist('module')[i]:
                module = Module.objects.get(id__iexact=request.POST.getlist('module')[i])
                quiz_bank.module = module
                quiz_bank.save()
                course = module.course
            i += 1
        return redirect(course)


class QuizTake(View):

    def get(self, request, quiz_bank_id):
        if request.user.is_anonymous:
            return redirect('/accounts/login')
        quiz_bank = QuizBank.objects.get(id=quiz_bank_id)
        print(quiz_bank)
        questions = list(Question.objects.filter(quizBank=quiz_bank))
        shuffle(questions)
        questions[:quiz_bank.required_questions_num]
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

                # creating CourseCompletion object to store course completion (surprise, surprise)
                CourseCompletion.objects.create(course=quiz_bank.course, learner=learner)
                course_completed = True
            learner.save()
            return render(request, "quiz/quiz_result.html", context={'result': result_percent,
                                                                     'course': quiz_bank.course,
                                                                     'course_completed': course_completed})
        fail = True        
        return render(request, "quiz/quiz_result.html", context={'fail': fail,
                                                                 'course': quiz_bank.course})