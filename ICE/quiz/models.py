from django.db import models
from courses.models import Course, Module
# Create your models here.


class QuizBank(models.Model):
    title = models.CharField(max_length=50, db_index=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True)
    required_questions_num = models.IntegerField()
    pass_rate = models.IntegerField()
    # sets module filed to NULL when module is deleted
    module = models.ForeignKey(Module, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.title


class Question(models.Model):
    body = models.CharField(max_length=100)
    quizBank = models.ForeignKey(QuizBank, on_delete=models.CASCADE)

    def __str__(self):
        return self.body


# stores answer options
class AnswerOptions(models.Model):
    body = models.CharField(max_length=50)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    # indicates whether provided answer option is actually a correct answer or not
    correct_incorrect = models.BooleanField()

    def __str__(self):
        return self.body

