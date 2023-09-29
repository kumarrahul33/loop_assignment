from django.db import models
# from rest_framework import 

# Create your models here.
# make a model containing the following fe
class ReportGen(models.Model):
    reportID = models.IntegerField(unique=True)
    status = models.BooleanField(default=False)
    report = models.JSONField(default=dict)
