from django.shortcuts import render
from django.http import HttpResponse

def HomeView(request):
    return render(request,'home.html')

def UploadFilesView(request):
    return render(request, 'upload_files.html')

