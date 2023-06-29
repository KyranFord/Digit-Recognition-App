"""
Definition of urls for Digit_Recognition_App.
"""

from datetime import datetime
from django.urls import path
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from app import forms, views


urlpatterns = [
    path('classify/', views.classify, name='classify'),
    path('', views.home, name='home'),
]
