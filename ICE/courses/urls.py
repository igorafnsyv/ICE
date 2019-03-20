#pattern match urls here
from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.courses_list),
    path('course/<str:slug>', views.course_detail, name = "course_detail_url"),
    path('create_module/<str:id>', views.ModuleCreate.as_view(), name = "create_module_url"),
    path('create_component/<str:id>', views.ComponentCreate.as_view(), name = "create_component_url")
]