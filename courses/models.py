from django.db import models
from django.shortcuts import reverse
# Create your models here.

class Course(models.Model):
    title = models.CharField(max_length = 150, db_index = True)
    description = models.TextField(blank = False)
    slug = models.SlugField(max_length=150, unique = True) #later actually can change
    #Instructor
    instructor = models.CharField(max_length = 40, db_index = True) #later link it ot actual instructor
    #current_Learners -> learners who are taking course now
    #completed_Learners learner who has already completed the course
    credit_units = models.IntegerField(db_index = True)
    status = models.IntegerField(db_index = True) # value 1 if course is opened, 0 if closed
    category = models.CharField(max_length = 150, db_index = True)

    def get_absolute_url(self):
        return reverse('course_detail_url', kwargs = {'slug' : self.slug})

    def __str__(self):
        return '{}'.format(self.title)


class Module(models.Model):
    title = models.CharField(max_length = 150, db_index = True)
    slug = models.SlugField(max_length= 50, db_index= True) 
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    #components
    position = models.IntegerField(db_index = True)
    #quiz bank
    #quiz

    def __str__(self):
        return '{}'.format(self.title)


class Component(models.Model):
    title = models.CharField(max_length = 50, db_index = True)
    body = models.TextField(blank = True) #either Text component or image component
    image = models.ImageField(upload_to = 'images/')
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add = True) #needs to keep constant somehow
    date_update = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return '{}'.format(self.title) #limit it to several symbols?

