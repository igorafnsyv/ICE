from django import forms
from .models import AnswerOptions, QuizBank, Question
#from quiz.models import QuizBank
from django.core.exceptions import ValidationError

class QuizForm(forms.ModelForm):
    class Meta:
        model = QuizBank
        fields = ['module', 'id']
        