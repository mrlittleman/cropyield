import sqlite3

import warnings
warnings.filterwarnings('ignore')
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor

from io import BytesIO
import base64
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
import csv, io
import psycopg2
from .models import CsvUploads
from .forms import UserInputPredictions, CreateUserForm


@login_required(login_url='login')
def Dashboard(request):
    template = 'dashboard.html'
    conn = sqlite3.connect("db.sqlite3")
    data = pd.read_sql("SELECT * FROM app_csvuploads", conn)
    
    # Plot 1
    fig, axes = plt.subplots(1, 2, figsize=(12,5))
    sns.distplot(data['Temperatures'],color="purple",bins=15,hist_kws={'alpha':0.2}, ax=axes[0])
    sns.distplot(data['WindSpeeds'],color="green",bins=15,hist_kws={'alpha':0.2}, ax=axes[1])
    plot1_data = get_image_data(fig)
    
    # Plot 2
    fig, axes = plt.subplots(1, 2, figsize=(12,5))
    sns.distplot(data['Temperatures'],color="purple",bins=15,hist_kws={'alpha':0.2}, ax=axes[0])
    sns.distplot(data['Humidity'],color="green",bins=15,hist_kws={'alpha':0.2}, ax=axes[1])
    plot2_data = get_image_data(fig)
    
    # Plot 3
    fig, ax = plt.subplots(figsize=(12,5))
    sns.countplot(y='TypesOfCrops',data=data, palette="plasma_r", ax=ax)
    plot3_data = get_image_data(fig)
    
    # Plot 4
    fig = sns.pairplot(data, hue = 'TypesOfCrops')
    plot4_data = get_image_data(fig.fig)
    
    context = {'plot1_data': plot1_data, 'plot4_data': plot4_data}
    return render(request, template, context)

def get_image_data(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    return base64.b64encode(buf.read()).decode('utf-8')

@login_required(login_url='login')
def Data(request):
    template = 'data_file.html'
    data = CsvUploads.objects.all().values()
    context = {
        'data': data
    }
    return render(request, template, context)

@login_required(login_url='login')
def UploadFile(request): 
    template = 'upload_file.html'
    if request.method == "POST":
        uploaded_file = request.FILES.get('filename')
        if uploaded_file:
            if uploaded_file.name.endswith('.csv'):
                data_set = uploaded_file.read().decode('UTF-8')
                io_string = io.StringIO(data_set)
                next(io_string)
                for columns in csv.reader(io_string, delimiter=','):
                    _, created = CsvUploads.objects.update_or_create(
                    Domain = columns[0],
                    Area = columns[1],
                    Element	= columns[2],
                    Year = columns[3],
                    Temperatures = columns[4],
                    DewPoints = columns[5],
                    Humidity = columns[6],
                    WindSpeeds = columns[7],
                    Pressures = columns[8],
                    Percipitations = columns[9],
                    Date = columns[10],
                    TypesOfCrops = columns[11],
                    Unit = columns[12],
                    Value = columns[13],
                    Nutrients = columns[14],
                    Soil = columns[15],
                
                )
                    #columns.save()
                messages.success(request, 'Uploaded file successfully!')
            else:
                messages.error(request, 'Error file! please import a csv file.')
    return render(request, template)


@login_required(login_url='login')
def Prediction(request):
    template = 'prediction.html'
    form = UserInputPredictions(request.POST or None)

    if form.is_valid():
        # print(form)
        cleanData = form.cleaned_data
        UserInputData = CsvUploads(
            Domain = cleanData['Domain'],
            Area = cleanData['Area'],
            Element	= cleanData['Element'],
            Year = cleanData['Year'],
            Temperatures = cleanData['Temperatures'],
            DewPoints = cleanData['DewPoints'],
            Humidity = cleanData['Humidity'],
            WindSpeeds = cleanData['WindSpeeds'],
            Pressures = cleanData['Pressures'],
            Percipitations = cleanData['Percipitations'],
            Date = cleanData['Date'],
            TypesOfCrops = cleanData['TypesOfCrops'],
            Unit = cleanData['Unit'],
            Value = cleanData['Value'],
            Nutrients = cleanData['Nutrients'],
            Soil = cleanData['Soil'],
        )
        UserInputData.save()

        conn = sqlite3.connect("db.sqlite3")
        data = pd.read_sql("SELECT * FROM app_csvuploads", conn)
        df = data.drop(['Domain', 'Area', 'Element', 'Date', 'TypesOfCrops',  'Unit', 'Nutrients', 'Soil', 'Value'], axis=1)
        X = df.iloc[:,:-1]
        y = df.iloc[:,-1]
        X_train,X_test,Y_train,Y_test = train_test_split(X,y,test_size=0.2,random_state=100)
        forest = RandomForestRegressor(n_estimators=30, random_state=30)
        rf = forest.fit(X_train, Y_train)
        rounded_prediction = round(rf.score(X_train, Y_train), 2)
        messages.success(request, 'Crop Prediction would be: ' + str(rounded_prediction))
        return redirect('Prediction')
    else:
        form = UserInputPredictions()

    return render(request, template, {'form': form})


def login_view(request):
    if request.method == 'POST':
        # Get the username and password from the request
        email = request.POST['email']
        password = request.POST['password']
        # Authenticate the user
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            # Redirect the user to the next page or to a success page
            redirect('Dashboard')
    context = {}

    return render(request, 'registration/login.html', context)

def logout_view(request):
    # Redirect the user to the login page
    logout(request)
    return redirect('login')

def register_view(request):
    template = 'registration/registration.html'
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account was successfully registered')
            return redirect('login')
        else:
           form = CreateUserForm()
    return render(request, template, {'form': form})