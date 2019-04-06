#pattern match urls here
from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.SignUp.as_view(), name="sign_up_url"),
    path('registration/<str:email>/<str:type>', views.RegisterUser.as_view(), name='user_registration_url'),
]