# pattern match urls here
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('list/', views.courses_list, name='course_list_url'),
    path('course/<str:id>', views.course_detail, name='course_detail_url'),
    path('create_module/<str:course_id>', views.ModuleCreate.as_view(), name='create_module_url'),
    path('create_component/<str:module_id>', views.ComponentCreate.as_view(), name='add_component_url'),
    path('study_course/<str:course_id>/', views.study_course, name='study_course_url'),
    path('study_module/<str:id>/', views.study_module, name='module_details_url'),
    path('create_course/', views.CourseCreate.as_view(), name="create_course_url"),
    path('delete_module/<str:module_id>/', views.module_delete, name='delete_module_url'),
    path('delete_component/<str:component_id>/', views.component_delete, name='delete_component_url'),
    path('available_enrollment/', views.all_courses, name='courses_for_enrollment_url'),
    path('enroll/<str:course_id>/', views.course_enroll, name='enroll_in_course_url'),
    path('component_free/<str:component_id>/', views.component_remove_module, name='component_remove_module_url'),
    path('completed_courses/', views.completed_courses_list, name='completed_courses_list_url'),
    path('upload_component/<str:course_id>/', views.ComponentUpload.as_view(), name='component_upload_url'),
    path('manage_module/<str:module_id>/', views.ManageModule.as_view(), name='manage_module_url'),
    path('apply_element_position/<str:component_id>/<str:position>/<str:element_type>/', views.apply_element_position),
    path('manage_course/<str:course_id>/', views.ManageCourse.as_view(), name='manage_course_url'),
    path('new_module_save_positions/<str:component_id>/<str:position>/<str:course_id>/', views.new_module_add_components),

]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
