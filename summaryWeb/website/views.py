from django.shortcuts import render

# Create your views here.
def homePage(request):
    return render(request,'home.html',context={})

def articleReview(request):
	return render(request,'personCenter.html',context={})