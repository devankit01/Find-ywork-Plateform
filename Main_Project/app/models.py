
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.db.models.functions import Concat
from django.db.models import Value

# User model -> Firstname , Lastname , password , email , username
# Create your models here.
class UserProfile(models.Model):
    phone = models.CharField(max_length = 20)
    pincode = models.CharField(max_length = 10)
    address = models.CharField(max_length=250 , null = True, blank = True)
    gender = models.CharField(max_length=250 , null = True)
    username = models.ForeignKey(User , on_delete = models.CASCADE)





class WorkerProfile(models.Model):
    phone = models.CharField(max_length = 20)
    pincode = models.CharField(max_length = 10)
    address = models.CharField(max_length = 250 , null = True, blank = True)
    occupation = models.CharField(max_length = 100)
    experience = models.CharField(max_length = 100)
    rupees = models.CharField(max_length = 100)
    hourorday = models.CharField(max_length = 100)
    gender = models.CharField(max_length=250 , null = True)
    username = models.ForeignKey(User , on_delete = models.CASCADE)



class Work(models.Model):
    title = models.CharField(max_length = 100)
    description = models.TextField()
    category = models.CharField(max_length=40)
    maxamount = models.CharField(max_length=40)
    maxdays = models.CharField(max_length=40)
    date = models.DateTimeField(default=datetime.now(),blank=True)
    creator = models.ForeignKey(UserProfile ,on_delete = models.CASCADE)

class Bid(models.Model):
    proposal_price = models.CharField(max_length = 20)
    proposal_days = models.CharField(max_length = 20)
    work = models.ForeignKey('Work',on_delete = models.CASCADE)
    worker = models.ForeignKey('WorkerProfile', on_delete = models.CASCADE)
    isassigned = models.BooleanField(default=False)
    

class Rating(models.Model):
    work = models.ForeignKey('Work', on_delete = models.CASCADE)
    rating = models.DecimalField(decimal_places=1,max_digits=5)
    feedback = models.TextField()


