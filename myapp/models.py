from django.db import models
from django.contrib.postgres.fields import ArrayField

# Create your models here.

class Books(models.Model):
    url = models.CharField(max_length=255, blank=False, null=False, primary_key=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    isbn = models.CharField(max_length=255, blank=True, null=True)
    authors = ArrayField(models.CharField(max_length=255, blank=True, null=True))
    nopages = models.IntegerField(null=True)
    publisher = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)
    # mediaType = models.CharField(max_length=255, blank=True, null=True)
    released = models.CharField(max_length=255, blank=True, null=True)
    # characters = ArrayField(models.CharField(max_length=255, blank=True, null=True))
    # povCharacters = models.CharField(max_length=255, blank=True, null=True)