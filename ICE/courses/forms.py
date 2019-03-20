from django import forms
from .models import Course, Module, Component
from django.core.exceptions import ValidationError

class ModuleForm(forms.ModelForm):
    class Meta:
        model = Module
        fields = ['title', 'slug']



   # def save(self):
        #course = 
    #    new_module = Module.objects.create(title = self.cleaned_data['title'], slug = self.cleaned_data['slug'], course = self.cleaned_data['course'])
     #   return new_module

    
class ComponentForm(forms.ModelForm):
    class Meta:
        model = Component
        fields = ['module']
