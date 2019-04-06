from django.http import HttpResponse
from django.shortcuts import redirect

# either redirect user to courses list or to login page (depends whether user is loged in or not)
def redirect_courses (request):
    return redirect('course_list_url')
