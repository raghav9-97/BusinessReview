from django.db import models
from django.contrib.postgres.fields import ArrayField
from signup.models import UserDefined


# Create your models here.
class BusiModel(models.Model):
    Business = models.CharField(max_length=100)
    User = models.ForeignKey(UserDefined,on_delete=models.CASCADE,related_name='user1',default=0)
    Manager = models.ForeignKey(UserDefined,blank=True,on_delete=models.SET_NULL,null=True,related_name='user2')
    Address = models.TextField()
    Zomato_URL = models.CharField(max_length=250,unique=True)
    Google_URL = models.CharField(max_length=250,help_text='Google Maps URL address is required.',unique=True)
    TimeStamp = models.DateField(auto_now=True)

    class Meta:
        unique_together = ['Business','Address']

class ScrapedData(models.Model):
    Name = models.CharField(max_length=100)
    Bus = models.ForeignKey(BusiModel,on_delete=models.CASCADE)
    Id = models.CharField(primary_key=True,max_length=100,default='')
    Polarity = models.DecimalField(null=True, blank=True,max_digits=50,decimal_places=10)
    User = models.IntegerField(default=0)
    Review = models.TextField()
    TimeStamp = models.DateField(auto_now=True)
    Rating = models.CharField(max_length=100)
    Date = models.CharField(max_length=100)
