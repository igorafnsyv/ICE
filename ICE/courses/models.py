from django.db import models
from django.shortcuts import reverse
# Create your models here.

class Learner (models.Model):
    name = models.CharField(max_length = 50, db_index = True)
    email = models.EmailField(max_length = 50)
    #password
    staff_id = models.IntegerField()
    courses = models.ManyToManyField('Course', blank = True)
    completed_modules = models.ManyToManyField('Module', blank = True)

    def __str__(self):
        return self.name

class Instructor (models.Model):
    name = models.CharField(max_length = 50, db_index = True)
    email = models.EmailField(max_length = 50)
    #password
    introduction = models.TextField()

    def __str__(self):
        return self.name


class Course(models.Model):
    title = models.CharField(max_length = 150, db_index = True)
    description = models.TextField(blank = False)
    slug = models.SlugField(max_length=150, unique = True) #later actually can change
    
    instructor = models.CharField(max_length = 40, db_index = True) 

    #instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE)

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
    position = models.IntegerField(db_index = True)
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse('module_details_url', kwargs = {'id' : self.id})

    def __str__(self):
        return '{}'.format(self.title)


class Component(models.Model):
    
    title = models.CharField(max_length = 50, db_index = True)
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE)
    body = models.TextField(blank = True) #either Text component or image component
    image = models.ImageField(upload_to = 'images/', blank = True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null = True, blank = True)
    module = models.ForeignKey(Module, on_delete=models.CASCADE, null = True, blank = True)
    date_created = models.DateTimeField(auto_now_add = True) #needs to keep constant somehow
    date_update = models.DateTimeField(auto_now_add = True)
    position = models.IntegerField(null = True, blank = True)

    def __str__(self):
        return '{}'.format(self.title) #limit it to several symbols?

