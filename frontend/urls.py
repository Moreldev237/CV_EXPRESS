from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('auth', views.auth, name='auth'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('cv-builder', views.cv_builder, name='cv_builder'),
    path('cover-letter', views.cover_letter, name='cover_letter'),
]
