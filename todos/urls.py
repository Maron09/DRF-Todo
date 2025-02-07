from django.urls import path
from . import views



urlpatterns = [
    path('categories/', views.CategoryView.as_view()),
    path('category/<int:pk>/', views.CategoryDetail.as_view()),
    
    path('my_todos/', views.TodoView.as_view()),
    path('todos/<int:pk>/', views.TodoDetailView.as_view()),
]