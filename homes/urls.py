from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('inquiry/', views.submit_inquiry, name='submit_inquiry'),
]