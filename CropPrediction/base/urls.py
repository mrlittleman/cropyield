from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView, name="home"),
    path('home/', views.HomeView, name="home"),
    path('uploads-files/', views.UploadFilesView, name="upload-files"),
   
]
