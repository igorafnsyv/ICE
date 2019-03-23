from django.contrib import admin

# Register your models here.
from .models import Course, Module, Component, Learner
admin.site.register(Course)
admin.site.register(Module)
admin.site.register(Component)
admin.site.register(Learner)
