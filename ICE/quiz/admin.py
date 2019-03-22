from django.contrib import admin

# Register your models here.
from .models import QuizBank, Question, AnswerOptions
admin.site.register(QuizBank)
admin.site.register(Question)
admin.site.register(AnswerOptions)
