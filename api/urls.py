from django.urls import path
from . import views



urlpatterns = [
    path('register/', views.UserRegistration.as_view()),
    path('otp/', views.VerifyEmail.as_view()),
    path('login/', views.LoginView.as_view()),
]