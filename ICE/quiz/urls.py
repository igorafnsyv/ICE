#pattern match urls here
from django.urls import path
from . import views

urlpatterns = [
    path('add_quiz/<str:id>', views.QuizAdd.as_view(), name = 'add_quiz_url'),   
]

