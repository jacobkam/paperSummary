from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required 
# Create your views here.
def homePage(request):
	return render(request,'home.html',context={})

def articleReview(request):
	return render(request,'personCenter.html',context={})