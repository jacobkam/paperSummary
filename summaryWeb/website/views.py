from django.shortcuts import render
from django.contrib.auth.models import User
from website.models import *
from django.contrib.auth.decorators import login_required
from faker import Factory
# Create your views here.
def homePage(request):
	#user1 = User.objects.create_user(username='jingxin',password='fujingxin')
	#user1.save()
	# user1= User.objects.get(username='jingxin')
	# #userProfile1 = UserProfile.objects.create(belong_to=user1,nick_name=user1.username)
	# #userProfile1.save()
	# userProfile1 = UserProfile.objects.get(belong_to_id=user1.id)
	# print(userProfile1.profile_image_url)
	# # #userProfile1.save()
	# # # # # # # user1.save()
	# # # # # # user1 = User.objects.create_user(username='jingxin',password='fujingxin')
	# # # # # # user1.save()
	# #Article.objects.all().delete()
	# #print(Comment.objects.all())
	# #print(Comment.objects.all())
	# fake = Factory.create()
	# for i in range(1,20):
	#     v = Article(
	#         tag='Drug response and resistance',
	#         title=fake.text(max_nb_chars=50),
	#         content=fake.text(max_nb_chars=3000),
	#         pubmedID=fake.text(max_nb_chars=10),
	#         belong_to=user1,
	#         )
	#     v.save()
	#     c = Comment(
	#         username=user1.username,
	#         article=v,
	#         profile_image=userProfile1.profile_image_url,
	#         user=user1,
	#         content=fake.text(max_nb_chars=300),
	#         )
	#     c.save()
	#     t = Ticket(
	#         voter=user1,
	#         article=v,
	#         )
	#     t.save()
	return render(request,'home.html',context={})

def articleReview(request):
	return render(request,'personCenter.html',context={})

def articleList(request):
	return render(request,'ariticleList.html',context={})

def detail(request):
	return render(request,'detail.html',context={})
def editing(request):
	return render(request,'edit.html',context={})

def review(request):
	return render(request,'review.html',context={})

def reviewDetial(request):
	return render(request,'reviewDetail.html',context={})