from django.urls import path
from . import views

urlpatterns = [
    path('', views.Dashboard, name="Dashboard"),
    path('Dashboard/', views.Dashboard, name="Dashboard"),
    path('Upload/', views.UploadFile, name="Upload"),
    path('Prediction/', views.Prediction, name="Prediction"),
    path('Data/', views.Data, name="Data"),
    path('login/', views.login_view, name='login'),
    path('Register', views.register_view, name="Register"),
    path('logout/', views.logout_view, name='logout'),
]