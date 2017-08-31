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

@api_view(['POST'])
@csrf_exempt
def login(request):
	serializers = StudentSerializers(data=request.data)
	if serializers.is_valid():
		name = serializers.initial_data['name']
		password = serializers.initial_data['passwd']

		# validation check
		user = authenticate(username=name,password=password)
		if user:
			body={
			'msg':'success',
			'success':1,
			}
			return Response(body,status=HTTP_2OO_OK)
		else:
			body={
			'user does not exist Or your password is wrong!',
			'success':2,
			}
			return Response(body,status=HTTP_404_NOT_FOUND)
	else:
		body={
		'msg':serializers.errors,
		'success':3,
		}
		return Response(body,status=status.HTTP_400_BAD_REQUEST)