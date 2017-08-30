from website.models import Student,Article
from rest_framework import serializers,status
from rest_framework.reponse import Response
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User

class StudentSerializers(serializers.ModelSerializer):
    name = serializers.CharField(min_length=1)
    class Meta:
        model = Student
        fields = '__all__'

class ArticleSerializers(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = '__all__'
