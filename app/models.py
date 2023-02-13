from django.db import models

# Create your models here.
class CsvUploads(models.Model):
    Domain = models.CharField(max_length=300)
    Area = models.CharField(max_length=300)
    Element = models.CharField(max_length=300)
    Year = models.PositiveSmallIntegerField()
    Temperatures = models.FloatField()
    DewPoints = models.FloatField()
    Humidity = models.PositiveSmallIntegerField()
    WindSpeeds = models.FloatField()
    Pressures = models.FloatField()
    Percipitations = models.FloatField()
    Date = models.CharField(max_length=300)
    TypesOfCrops = models.CharField(max_length=300)
    Unit = models.CharField(max_length=50)
    Value = models.CharField(max_length=300)
    Nutrients = models.CharField(max_length=300)
    Soil = models.CharField(max_length=300)