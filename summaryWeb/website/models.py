from django.db import models
from django.contrib.auth.models import User
from datetime import date
#from faker import Factory
# Create your models here.
class UserProfile(models.Model):
    belong_to = models.OneToOneField(to=User,related_name='userprofile')
    profile_image = models.URLField('imgURL',max_length=100,blank=True,null=True)
    nick_name = models.CharField('nickName',max_length=100, blank=True, null=True,unique=True)
    is_admin = models.BooleanField('admin',default=False)

    def __str__(self):
        return self.nick_name

class Article(models.Model):
    title = models.CharField(null=False,max_length=50)
    createDate = models.DateField(default=date.today)
    pubmedID=models.CharField(null=False,max_length=50)
    content = models.TextField()
    belong_to = models.ForeignKey(to=User,related_name='Article')
    vote = models.IntegerField(default=0)
    commentCount = models.IntegerField(default=0)

    CHOOOSE = (
        ('Cancer immunology','Cancer immunology'),
        ('Cancer Epigenetics','Cancer Epigenetics'),
        ('CRISPR screens','CRISPR screens'),
        ('Drug response and resistance','Drug response and resistance'),
    )
    tag = models.CharField('tag',choices=CHOOOSE,max_length=10,blank=True,null=True)
    def __str__(self):
        return self.title

class Comment(models.Model):
    article = models.ForeignKey(to=Article,related_name='comment')
    user = models.ForeignKey(to=User,related_name='comment')
    content=models.TextField(default=None)
    createDate = models.DateField(default=date.today)

class Ticket(models.Model):
    voter = models.ForeignKey(to=User,related_name='voted_tickets')
    article = models.ForeignKey(to=Article,related_name='tickes')
    like = models.BooleanField(default=False, verbose_name='like')


# user1 = User.objects.get(username='jingxin')

# # # # # user1.save()
# # # # user1 = User.objects.create_user(username='jingxin',password='fujingxin')
# # # # user1.save()
# # Article.objects.all().delete()
# fake = Factory.create()
# for i in range(1,20):
#     v = Article(
#         tag='Drug response and resistance',
#         title=fake.text(max_nb_chars=50),
#         content=fake.text(max_nb_chars=3000),
#         pubmedID=fake.text(max_nb_chars=50),
#         belong_to=user1,
#         )
#     v.save()
# fake = Factory.create()
# for i in range(39,50):
#     article1=Article.objects.get(id=i)
#     v = Comment(
#         article=article1,
#         user=user1,
#         content=fake.text(max_nb_chars=300),
#         )
#     v.save()
