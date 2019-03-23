#pattern match urls here
from django.urls import path
from . import views

urlpatterns = [
    path('add_quiz/<str:id>', views.QuizAdd.as_view(), name = 'add_quiz_url'),
    path('take_quiz/<str:quiz_bank_id>', views.QuizTake.as_view(), name = 'take_quiz_url'),   
]

