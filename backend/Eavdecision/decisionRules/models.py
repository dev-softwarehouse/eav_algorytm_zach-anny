from django.db import models

# Create your models here.
class File(models.Model):
    file = models.FileField()

class Eva(models.Model):
    attribute = models.CharField(max_length=250,null=True, blank=True)
    value = models.CharField(max_length=250)
    decision = models.CharField(max_length=250)
    row = models.CharField(max_length=250)
    
class decisionValue(models.Model):
    value = models.CharField(max_length=250)
    
    
    