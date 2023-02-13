from django.db import models

# Create your models here.
class CsvUploads(models.Model):
    Domain = models.CharField(max_length=100)
    Area = models.CharField(max_length=100)
    Element = models.CharField(max_length=100)
    Year = models.PositiveSmallIntegerField()
    Temperatures = models.FloatField()
    DewPoints = models.FloatField()
    Humidity = models.PositiveSmallIntegerField()
    WindSpeeds = models.FloatField()
    Pressures = models.FloatField()
    Percipitations = models.FloatField()
    Date = models.CharField(max_length=100)
    TypesOfCrops = models.CharField(max_length=100)
    Unit = models.CharField(max_length=50)
    Value = models.CharField(max_length=100)
    Nutrients = models.CharField(max_length=100)
    Soil = models.CharField(max_length=100)