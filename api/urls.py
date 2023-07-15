from django import views
from django.urls import path
from . import views
urlpatterns = [
    path('happyeid/', views.write_Name_Image,name='happyeidImage')
]