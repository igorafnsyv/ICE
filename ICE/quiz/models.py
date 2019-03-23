from django.db import models
from django.shortcuts import reverse
from courses.models import Course, Module
# Create your models here.
class QuizBank(models.Model):
    title = models.CharField(max_length = 50, db_index = True)
    #instuctor
    required_questions_num = models.IntegerField()
    pass_rate = models.IntegerField()
    module = models.ForeignKey(Module, on_delete = models.CASCADE, null = True, blank = True)
    #questions
    def __str__(self):
        return self.title


class Question(models.Model):
    body = models.CharField(max_length = 100)
    quizBank = models.ForeignKey(QuizBank, on_delete= models.CASCADE)

    def __str__(self):
        return self.body

class AnswerOptions(models.Model):  #stores answer options
    body = models.CharField(max_length = 50)
    question = models.ForeignKey(Question, on_delete= models.CASCADE)
    correct_incorrect = models.BooleanField()#indicates whether provided answer option is actually a correct answer or not

    def __str__(self):
        return self.body

