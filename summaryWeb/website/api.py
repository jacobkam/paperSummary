from rest_framework import serializers,status
from rest_framework.response import Response
from rest_framework.decorators import api_view,authentication_classes
from django.contrib.auth.models import User
from website.serializers import *
from website.models import *
from rest_framework.authtoken.models import Token
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth import authenticate,login
import datetime


@api_view(['POST'])
@csrf_exempt
def login(request):

	serializers = UserSerializers(data=request.data)
	if serializers.is_valid():
		username = serializers.initial_data['username']
		password = serializers.initial_data['password']
		# validation check

		user = authenticate(username=username,password=password)

		if user:
			token,created = Token.objects.get_or_create(user=user)
			print(token)
			if not created:
			# update the created time of the token to keep it valid
				token.created = datetime.datetime.utcnow()
				token.save()

			body={
			'msg':'success',
			'success':1,
			'token':token.key,
			}
			return Response(body,status=status.HTTP_200_OK)
		else:
			# determine if user is existed
			try:
				user_is_exist = User.objects.get(username=username)
				body={
					'msg':'password is wrong!',
					'success':2,
				}
			except:
				body={
					'msg':'User does not exist!',
					'success':3,
				}

			return Response(body,status=status.HTTP_404_NOT_FOUND)
	else:
		body={
		'msg':serializers.errors,
		'success':4,
		}
		return Response(body,status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
def article(request):
	# print ('auth is :',request.auth)
	# print ('user is :',request.user)
	# print(request.user.id)
	if request.method == 'GET':
		if request.auth:
			personalArticle = Article.objects.filter(belong_to_id=request.user.id)
			#print(Article.objects.filter(id__in=[1,2]))
			try:
				user_like = Ticket.ojects.filter(voter_id=request.user.id,like=True)
				user_like_article_id = list(map(lambda x: x['article_id'],list(user_like.values('article_id').distinct())))
				favoriteArticle = Article.objects.filter(id__in=user_like_article_id)
				favoriteArticleQueryset=ArticleSerializers(favoriteArticle, many=True).data
			except:
				favoriteArticleQueryset=''

			personalArticleQueryset = ArticleSerializers(personalArticle, many=True)

			body={
				'personalArticle':personalArticleQueryset.data,
				'favoriteArticle':favoriteArticleQueryset,
			}
			return Response(body, status=status.HTTP_200_OK)
		else:
			body = {
			    'msg':'Sorry,Please login first',
			}
			return Response(body, status=status.HTTP_403_FORBIDDEN)


@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
def allArticle(request):
    if request.method == 'GET':
        if request.auth:
        	now = datetime.date.today()
        	lastMonday = now - datetime.timedelta(datetime.date.today().weekday()+7)
        	article = Article.objects.filter(createDate__lt=lastMonday).order_by('-vote')
        	articleQueryset = ArticleSerializers(article,many=True)
        	return Response(articleQueryset.data,status=status.HTTP_200_OK)
        else:
            body = {
            'msg':'Sorry,Please login first',
            }
            return Response(body, status=status.HTTP_403_FORBIDDEN)

            
@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
def reviewArticle(request):
	if request.method == 'GET':
	    if request.auth:
	    	# compute date
	    	now = datetime.date.today()
	    	lastMonday = now - datetime.timedelta(datetime.date.today().weekday()+7)
	    	article = Article.objects.filter(createDate__gte=lastMonday).order_by('-createDate')
	    	articleQueryset = ArticleSerializers(article,many=True)
	    	return Response(articleQueryset.data,status=status.HTTP_200_OK)
	    else:
	        body = {
	        'msg':'Sorry,Please login first',
	        }
	        return Response(body, status=status.HTTP_403_FORBIDDEN)


@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
def articleDetail(request,id):
    if request.method == 'GET':
        if request.auth:
            article = Article.objects.get(id=id)
            articleQueryset = ArticleSerializers(article,many=False)
            return Response(articleQueryset.data,status=status.HTTP_200_OK)
        else:
            body = {
            'msg':'Sorry,Please login first',
            }
            return Response(body, status=status.HTTP_403_FORBIDDEN)



@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
def revDetail(request,id):
    if request.method == 'GET':
        if request.auth:
            article = Article.objects.get(id=id)
            comment = Comment.objects.get(article_id=id,user_id=request.user.id)
            articleQueryset = ArticleSerializers(article,many=False)
            commentQueryset = CommentSerilizers(comment)
            body={
            'article':articleQueryset.data,
            'comment':commentQueryset.data,
            }
            return Response(body,status=status.HTTP_200_OK)
        else:
            body = {
            'msg':'Sorry,Please login first',
            }
            return Response(body, status=status.HTTP_403_FORBIDDEN)

