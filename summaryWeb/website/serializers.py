from django.contrib.auth.models import User
from website.models import *
from rest_framework import serializers


class UserProfileSerializers(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = "__all__"


class ArticleSerializers(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = '__all__'

class UserSerializers(serializers.ModelSerializer):
    username = serializers.CharField(min_length=3,max_length=20)
    password = serializers.CharField(min_length=6,max_length=20)

    class Meta:
        model = User
        fields = "__all__"

class TicketSerializers(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = '__all__'

class CommentSerilizers(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
