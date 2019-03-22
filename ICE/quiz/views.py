from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import QuizBank, Question, AnswerOptions

from courses.models import Module

from .forms import QuizForm

from django.views.generic import View


# Create your views here.
class QuizAdd(View):

    def get(self, request, id):
        module = Module.objects.get(id__iexact = id)
        quiz_banks = QuizBank.objects.filter(module = None)    #either no Module assigned or no course assigned
        quiz_bank_form = QuizForm()
        return render (request, 'quiz/add_existing_quiz_bank.html', context = {'module' : module, 'quiz_banks' : quiz_banks, 'form' : quiz_bank_form}) 

    def post(self, request, id):
        module = Module.objects.filter(id__iexact = id)
        print()
        print(request.POST)
        print()
        i = 0
        course = module[0].course
        for quiz_bank_id in request.POST.getlist('quiz_bank_id'):
            quiz_bank = QuizBank.objects.get(id__iexact = quiz_bank_id)
            if request.POST.getlist('module')[i]:
                module = Module.objects.get(id__iexact = request.POST.getlist('module')[i])
                quiz_bank.module = module
                quiz_bank.save()
                course = module.course
            i += 1


        return redirect(course)
