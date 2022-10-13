from django.urls import path

from . import views

urlpatterns=[
    path('', views.toLogin),
    path('index/', views.login),
    path('toRegister/', views.toRegister),
    path('register/', views.register),
    path('student/login', views.StudentLogin),
    path('student/register', views.StudentRegister),
]
