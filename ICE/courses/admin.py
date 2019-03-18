from django.contrib import admin

# Register your models here.
from .models import Course, Module, Component
admin.site.register(Course)
admin.site.register(Module)
admin.site.register(Component)