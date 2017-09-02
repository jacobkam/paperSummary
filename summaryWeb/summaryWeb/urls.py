"""summaryWeb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from website.views import homePage,articleReview,articleList,detail,editing
from website.api import login,article,allArticle,articleDetail

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^home/', homePage,name='home'),
    url(r'^$', homePage,name='home'),
    url(r'^article/$', articleReview,name='articleReview'),
    url(r'^articleList/$', articleList,name='articleList'),
    url(r'^detail/',detail,name='detail'),
    url(r'^editing/',editing,name='editing'),

    ## api
    url(r'^api/login/', login),
    url(r'^api/article/', article),
    url(r'^api/allArticle/', allArticle),
    url(r'^api/detail/(?P<id>\d+)',articleDetail),# get detail
]
