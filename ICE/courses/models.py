from django.db import models
from django.shortcuts import reverse

from django.contrib.auth.models import User
# Create your models here.


class Category(models.Model):
    title = models.CharField(max_length=50, db_index=True, blank=True, null=True)

    def __str__(self):
        return self.title


class Learner (models.Model):
    first_name = models.CharField(max_length=50, db_index=True)
    last_name = models.CharField(max_length=50, db_index=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    staff_id = models.CharField(max_length=8, db_index=True)
    courses = models.ManyToManyField('Course', blank=True)
    email = models.EmailField(max_length=50, blank=True, null=True)
    completed_modules = models.ManyToManyField('Module', blank=True)

    def __str__(self):
        return self.first_name + " " + self.last_name


class Instructor (models.Model):
    first_name = models.CharField(max_length=50, db_index=True)
    last_name = models.CharField(max_length=50, db_index=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    introduction = models.TextField()
    email = models.EmailField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.first_name + " " + self.last_name


class Course(models.Model):
    title = models.CharField(max_length=150, db_index=True)
    description = models.TextField(blank=False)
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE)
    # to find current learners -> learners - course_completions
    credit_units = models.IntegerField(db_index=True, null=True, blank=True)

    # value 1 if course is opened, 0 if closed
    status = models.IntegerField(db_index=True, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)

    def get_absolute_url(self):
        return reverse('course_detail_url', kwargs={'course_id': self.id})

    def __str__(self):
        return '{}'.format(self.title)


# To record course completion.
class CourseCompletion(models.Model):
    learner = models.ForeignKey(Learner, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date_completed = models.DateTimeField(auto_now_add=True)
    cumulative_credits = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.learner.first_name + ' ' + self.learner.last_name + ' ' + self.course.title


class Module(models.Model):

    title = models.CharField(max_length=150, db_index=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True)
    position = models.IntegerField(db_index=True, null=True, blank=True)
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE, blank=True, null=True)

    def get_absolute_url(self):
        return reverse('module_details_url', kwargs={'module_id': self.id})

    def __str__(self):
        return '{}'.format(self.title)


class Component(models.Model):
    
    title = models.CharField(max_length=50, db_index=True)
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE)

    # either Text component or image component
    body = models.TextField(blank=True)
    image = models.ImageField(upload_to='images/', blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True)
    module = models.ForeignKey(Module, on_delete=models.CASCADE, null=True, blank=True)

    # todo date_created must be kept constant, while date_update is var
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now_add=True)
    position = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return '{}'.format(self.title)
