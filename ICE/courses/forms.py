from django import forms
from .models import Course, Module, Component
#from quiz.models import QuizBank
from django.core.exceptions import ValidationError


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'description', 'credit_units', 'category' ]

class ModuleForm(forms.ModelForm):
    class Meta:
        model = Module
        fields = ['title']



   # def save(self):
        #course = 
    #    new_module = Module.objects.create(title = self.cleaned_data['title'], slug = self.cleaned_data['slug'], course = self.cleaned_data['course'])
     #   return new_module

    
class ComponentForm(forms.ModelForm):
    class Meta:
        model = Component
        fields = ['module', 'id']
 #   title = forms.IntegerField(widget=forms.HiddenInput)
