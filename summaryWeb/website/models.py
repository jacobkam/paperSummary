from django.db import models
from django.contrib.auth.models import User
from datetime import date
# Create your models here.
class Student(models.Model):
    name = models.CharField(null=False,max_length=50)
    belong_to = models.OneToOneField(to=User,related_name='Student')
    def __str__(self):
        return self.name

class Article(models.Model):
    title = models.CharField(null=False,max_length=50)
    createDate = models.DateField(default=date.today)
    pubmedID=models.CharField(null=False,max_length=50)
    content = models.TextField()
    comment = models.TextField()
    belong_to = models.ForeignKey(to=Student,related_name='Article')
    vote = models.IntegerField()
    def __str__(self):
        return self.title

class Ticket(models.Model):
    voter = models.ForeignKey(to=Student,related_name='voted_tickets')
    article = models.ForeignKey(to=Article,related_name='tickes')
    like = models.BooleanField(default=False, verbose_name='like')
