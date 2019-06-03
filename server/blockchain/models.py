from django.db import models

class Block(models.Model):
    creatorID = models.CharField(max_length=100)
    objectID = models.CharField(max_length=100)
    objectType = models.CharField(max_length=100)
    pfand = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    prevhash = models.CharField(max_length=100)

class Company(models.Model):
    ID = models.CharField(max_length=100) #Generated internal ID
    name = models.CharField(max_length=100)
    adress = models.CharField(max_length=100)
    companyRegistrationNumber = models.CharField(max_length=100) #The registration number every company owns
    dateOfRegistration = models.CharField(max_length=100)
    permission = models.CharField(max_length=100) #Is a scrapper or company?