from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
# Create your views here.
def homePage(request):
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