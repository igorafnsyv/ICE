#pattern match urls here
from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.courses_list, name = "course_list_url"),
    path('course/<str:id>', views.course_detail, name = "course_detail_url"),
    path('create_module/<str:id>', views.ModuleCreate.as_view(), name = "create_module_url"),
    path('create_component/<str:id>', views.ComponentCreate.as_view(), name = "add_component_url"),
    path('course_list/', views.learner_course_list),
    path('study_course/<str:id>/', views.study_course, name = "study_course_url"),
    path('study_module/<str:id>/', views.study_module , name = "module_details_url"),
    path('create_course/', views.CourseCreate.as_view(), name = "create_course_url"),

]
