from django import forms
from .models import Course, Module, Component
#from quiz.models import QuizBank
from django.core.exceptions import ValidationError


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'description', 'credit_units', 'category']


class ModuleForm(forms.ModelForm):
    class Meta:
        model = Module
        fields = ['title', 'position']


class ComponentForm(forms.ModelForm):
    class Meta:
        model = Component
        fields = ['module', 'id']


class ComponentUploadForm(forms.ModelForm):
    class Meta:
        model = Component
        fields = ['title', 'body', 'image']
