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
from django.core.files.base import ContentFile
#from PIL import Image
# for delete files
import os
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

@api_view(['POST'])
@csrf_exempt
def login(request):
	serializers = UserSerializers(data=request.data)
	#Article.objects.get(id=71).delete()
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
			now = datetime.date.today()
			lastMonday = now - datetime.timedelta(datetime.date.today().weekday()+7)
			article = Article.objects.filter(createDate__lte=lastMonday).order_by('-createDate')
			personalArticle = article.filter(belong_to_id=request.user.id)
			try:
				userprofile = UserProfile.objects.get(belong_to_id=request.user.id)
			except:
				userNow1= User.objects.get(id=request.user.id)
				userprofile=UserProfile.objects.create(belong_to=userNow1,nick_name=userNow1.username,is_admin=userNow1.is_superuser)
				userprofile.save()
			userprofileQueryset = UserProfileSerializers(userprofile)
			#print(Article.objects.filter(id__in=[1,2]))
			try:
				user_like = Ticket.objects.filter(voter_id=request.user.id,like=True)
				user_like_article_id = list(user_like.values_list('article_id',flat=True).distinct())
				print(user_like_article_id)
				favoriteArticle = article.filter(id__in=user_like_article_id)
				favoriteArticleQueryset=ArticleSerializers(favoriteArticle, many=True).data

			except:
				favoriteArticleQueryset=''

			personalArticleQueryset = ArticleSerializers(personalArticle, many=True).data
			

			body={
				'personalArticle':personalArticleQueryset,
				'favoriteArticle':favoriteArticleQueryset,
				'userprofile':userprofileQueryset.data,
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
        	article = Article.objects.filter(createDate__lte=lastMonday).filter(is_saveToEdit=False).order_by('-vote')
        	articleQueryset = ArticleSerializers(article,many=True).data
        	return Response(articleQueryset,status=status.HTTP_200_OK)
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
	    	article = Article.objects.filter(createDate__gte=lastMonday).filter(is_saveToEdit=False).order_by('-createDate')
	    	articleQueryset = ArticleSerializers(article,many=True).data
	    	return Response(articleQueryset,status=status.HTTP_200_OK)
	    else:
	        body = {
	        'msg':'Sorry,Please login first',
	        }
	        return Response(body, status=status.HTTP_403_FORBIDDEN)


@api_view(['GET','PUT','POST'])
@authentication_classes((TokenAuthentication,))
def articleDetail(request,id):
    if request.method == 'GET':
        if request.auth:
            article = Article.objects.get(id=id)
            article.pubmedIDurl='https://www.ncbi.nlm.nih.gov/pubmed/'+article.pubmedID
            article.save()
            #Ticket.objects.all().delete()
            try:
            	comment = Comment.objects.filter(article_id=id)
            	commentQueryset = CommentSerilizers(comment,many=True).data
            except:
            	commentQueryset=''
            try:
            	ticket = Ticket.objects.get(article_id=id,voter_id=request.user.id)
            except:
            	userNow = User.objects.get(id=request.user.id)
            	ticket_new = Ticket(article=article,voter=userNow)
            	ticket_new.save()
            	ticket = ticket_new
            articleQueryset = ArticleSerializers(article,many=False).data
            ticketQueryset = TicketSerializers(ticket,many=False)

            body={
            'article':articleQueryset,
            'comment':commentQueryset,
            'ticket':ticketQueryset.data,
            }
            return Response(body,status=status.HTTP_200_OK)

    elif request.method == 'PUT':
    	print(request.data)
    	if request.auth:
    		ticket = Ticket.objects.get(article_id=id,voter_id=request.user.id)
    		ticket.like = not ticket.like
    		ticket.save()

    		article = Article.objects.get(id=id)
    		article_own_userprofile=UserProfile.objects.get(belong_to_id=article.belong_to_id)

    		article.vote += 1 if ticket.like else -1
    		article.save()

    		article_own_userprofile.like_count += 1 if ticket.like else -1
    		article_own_userprofile.save()
    		ticketQueryset = TicketSerializers(ticket,many=False)
    		body={
    		'ticket':ticketQueryset.data,
    		'vote':article.vote,
    		}
    		return Response(body,status=status.HTTP_200_OK)
    	else:
    		body = {'msg':'Sorry,Please login first',}
    		return Response(body, status=status.HTTP_403_FORBIDDEN)

    elif request.method == 'POST':
    	if request.auth:
   			serializers = CommentSerilizers(data=request.data)
   			print(serializers.initial_data['content'])
   			content = serializers.initial_data['content']
   			user = User.objects.get(id=request.user.id)
   			userprofile = UserProfile.objects.get(belong_to_id=request.user.id)
   			article=Article.objects.get(id=id)
   			newComment = Comment(username=user.username,content=content,user=user,article=article,profile_image=userprofile.profile_image_url)
   			newComment.save()
   			article.commentCount += 1
   			article.save()
   			userprofile.comment_count += 1
   			userprofile.save()
   			comments = Comment.objects.filter(article_id=id,user_id=request.user.id)
   			commentQueryset=CommentSerilizers(comments,many=True)
   			body={
   			'comment':commentQueryset.data,
   			'commentCount':article.commentCount,
   			}
   			return Response(body,status=status.HTTP_200_OK)


@api_view(['GET','PUT','POST'])
@authentication_classes((TokenAuthentication,))
def revDetail(request,id):
    if request.method == 'GET':
        if request.auth:
            article = Article.objects.get(id=id)
            article.pubmedIDurl='https://www.ncbi.nlm.nih.gov/pubmed/'+article.pubmedID
            article.save()
            #Ticket.objects.all().delete()
            try:
            	comment = Comment.objects.filter(article_id=id,user_id=request.user.id)
            	commentQueryset = CommentSerilizers(comment,many=True).data
            except:
            	commentQueryset=''
            try:
            	ticket = Ticket.objects.get(article_id=id,voter_id=request.user.id)
            except:
            	userNow = User.objects.get(id=request.user.id)
            	ticket_new = Ticket(article=article,voter=userNow)
            	ticket_new.save()
            	ticket = ticket_new
            articleQueryset = ArticleSerializers(article,many=False).data
            ticketQueryset = TicketSerializers(ticket,many=False)

            body={
            'article':articleQueryset,
            'comment':commentQueryset,
            'ticket':ticketQueryset.data,
            }
            return Response(body,status=status.HTTP_200_OK)
        else:
            body = {
            'msg':'Sorry,Please login first',
            }
            return Response(body, status=status.HTTP_403_FORBIDDEN)

    elif request.method == 'PUT':
    	if request.auth:
    		ticket = Ticket.objects.get(article_id=id,voter_id=request.user.id)
    		ticket.like = not ticket.like
    		ticket.save()

    		article = Article.objects.get(id=id)
    		article_own_userprofile=UserProfile.objects.get(belong_to_id=article.belong_to_id)

    		article.vote += 1 if ticket.like else -1
    		article.save()

    		article_own_userprofile.like_count += 1 if ticket.like else -1
    		article_own_userprofile.save()

    		ticketQueryset = TicketSerializers(ticket,many=False)
    		return Response(ticketQueryset.data,status=status.HTTP_200_OK)
    	else:
    		body = {'msg':'Sorry,Please login first',}
    		return Response(body, status=status.HTTP_403_FORBIDDEN)

    elif request.method == 'POST':
    	if request.auth:
   			serializers = CommentSerilizers(data=request.data)
   			print(serializers.initial_data['content'])
   			content = serializers.initial_data['content']
   			user = User.objects.get(id=request.user.id)
   			userprofile = UserProfile.objects.get(belong_to_id=request.user.id)
   			article=Article.objects.get(id=id)
   			newComment = Comment(username=user.username,content=content,user=user,article=article,profile_image=userprofile.profile_image_url)
   			newComment.save()
   			article.commentCount += 1
   			article.save()
   			userprofile.comment_count += 1
   			userprofile.save()
   			comments = Comment.objects.filter(article_id=id,user_id=request.user.id)
   			commentQueryset=CommentSerilizers(comments,many=True)
   			return Response(commentQueryset.data,status=status.HTTP_200_OK)

@api_view(['GET','POST'])
@authentication_classes((TokenAuthentication,))
def editPage(request):
	if request.method == 'GET':
		if request.auth:
			allArticles = Article.objects.filter(is_saveToEdit=False)
			#Article.objects.filter(belong_to_id=request.user.id,is_saveToEdit=True).delete()
			pubmeDids = list(map(lambda x: x['pubmedID'],list(allArticles.values('pubmedID'))))
			try:
				article = Article.objects.get(belong_to_id=request.user.id,is_saveToEdit=True)
				articleQueryset=ArticleSerializers(article,many=False).data
				articleQueryset['tag']=articleQueryset['tag'].split('-')
			except:
				articleQueryset=''
			body={
				'article':articleQueryset,
				'pubIDs':pubmeDids,
			}
			return Response(body,status=status.HTTP_200_OK)

	elif request.method == 'POST':
		authorTothisArticle = User.objects.get(id=request.user.id)
		serializers = ArticleSerializers(data=request.data)
		title = serializers.initial_data['title']
		content = serializers.initial_data['content']
		pubmedID = serializers.initial_data['pubmedID']
		user = User.objects.get(id=request.user.id)
		is_save = serializers.initial_data['save']
		tag = '-'.join(dict(request.data)['tag[]'])
		is_pubId_exist = Article.objects.filter(pubmedID=pubmedID)
		nameList = list(is_pubId_exist.values_list('authorName',flat=True).distinct())
		if len(is_pubId_exist) > 1 or len(nameList) > 1 or (authorTothisArticle.username not in nameList and len(nameList)==1):
			body={
			'msg':'Paper has been read before!'
			}
			return Response(body,status=status.HTTP_403_FORBIDDEN)

		try:
			# make sure save article are unique
			preArticle = Article.objects.get(belong_to_id=request.user.id,is_saveToEdit=True)
			print(is_save)
			preArticle.title=title
			preArticle.content=content
			preArticle.pubmedID=pubmedID
			preArticle.belong_to=user
			preArticle.is_saveToEdit=is_save
			preArticle.tag=tag
			preArticle.createDate=datetime.date.today()
			preArticle.authorName=authorTothisArticle.username
			preArticle.save()

		except:
			newArtcle = Article(
				title=title,
				content=content,
				pubmedID=pubmedID,
				belong_to=user,
				is_saveToEdit=is_save,
				tag=tag,
				createDate=datetime.date.today(),
				authorName=authorTothisArticle.username,
				)
			newArtcle.save()

		body={
		'msg':'success!',
		}
		return Response(body,status=status.HTTP_200_OK)

	else:
		body={
		'msg':'please login first!',
		}
		return response(body,status=status.HTTP_403_FORBIDDEN)

@api_view(['GET','POST'])
@authentication_classes((TokenAuthentication,))
def passwordAPI(request):
	if request.method == 'POST':
		if request.auth:
			serializers = UserSerializers(data=request.data)
			newPassword = serializers.initial_data['password']
			userNow = User.objects.get(id=request.user.id)
			userNow.set_password(newPassword)
			userNow.save()
			body={
			'msg':'change success!'
			}
			return Response(body,status=status.HTTP_200_OK)

@api_view(['GET','POST'])
@authentication_classes((TokenAuthentication,))
def imageAPI(request):
	if request.method == 'POST':
			if request.auth:
				imageProile= request.FILES['image']
				decodeIMG = ContentFile(imageProile.read())
				userNow = UserProfile.objects.get(belong_to_id=request.user.id)

				newFileName =userNow.nick_name + '.'+ imageProile.name.split('.')[-1]
				absolotePath = os.path.join(BASE_DIR,'website','static','upload','avatar',newFileName).replace("//", "/")
				print(absolotePath)
				if os.path.isfile(absolotePath):
					os.remove(absolotePath)
				userNow.profile_image.save(newFileName,content=decodeIMG)
				newImgURL = '/static/upload/avatar/'+userNow.nick_name + '.'+imageProile.name.split('.')[-1]
				userNow.profile_image_url = newImgURL
				userNow.save()
				Comment.objects.filter(user_id=request.user.id).update(profile_image=newImgURL)
				body={
				'msg':'change success!'
				}
				return Response(body,status=status.HTTP_200_OK)
	body={
	'msg':'Please provide a correct image file!'
	}
	return Response(body,status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','POST','PUT'])
@authentication_classes((TokenAuthentication,))
def adminPage(request):
	theUser = User.objects.get(id=request.user.id)
	if theUser.is_superuser:
		if request.method == 'GET':
			userAll = UserProfile.objects.all()
			userLike = UserProfileSerializers(userAll.order_by('-like_count'),many=True).data
			userComment = UserProfileSerializers(userAll.order_by('-comment_count'),many=True).data
			# who do not upload summary
			now = datetime.date.today()
			thisMonday=now - datetime.timedelta(datetime.date.today().weekday())
			lastMonday = now - datetime.timedelta(datetime.date.today().weekday()+7)
			uploadArticle = Article.objects.filter(createDate__gte=lastMonday).filter(createDate__lt=thisMonday).filter(is_saveToEdit=False)
			uploadUserID =list(uploadArticle.values_list('belong_to_id',flat=True).distinct())
			try:
				notSubmitUser = UserProfile.objects.exclude(belong_to_id__in=uploadUserID)
				notSubmitUserQuerySet = UserProfileSerializers(notSubmitUser,many=True).data
			except:
				notSubmitUserQuerySet=''
			body={
			'likeRank':userLike,
			'commentRank':userComment,
			'unSubmit':notSubmitUserQuerySet,
			}
			return Response(body,status.HTTP_200_OK)

		if request.method == 'POST':
			serializers = UserSerializers(data=request.data)
			username = serializers.initial_data['username']
			try:
				newUser = User.objects.create_user(username=username,password='12345678')
				newUser.save()
				newUser = User.objects.get(username=username)
				newUserProfile = UserProfile.objects.create(nick_name=username,belong_to=newUser)
				newUserProfile.save()
				body={
				'msg':'success!',
				}
				return Response(body,status=status.HTTP_200_OK)
			except:
				body={
				'msg':'The user existed!',
				}
				print(body)
				return Response(body,status=status.HTTP_400_BAD_REQUEST)

		if request.method == 'PUT':
			serializers = UserSerializers(data=request.data)
			username = serializers.initial_data['username']
			print(username)
			try:
				delelteUser = User.objects.get(username=username)
				try:
					Article.objects.filter(belong_to_id=delelteUser.id).delete()
					UserProfile.objects.filter(belong_to_id=delelteUser.id).delete()
				except:
					pass
				delelteUser.delete()
				body={
				'msg':'success!'
				}
				return Response(body,status=status.HTTP_200_OK)
			except:
				body={
				'msg':'The user does not exist!'
				}
				print(body)
				return Response(body,status=status.HTTP_400_BAD_REQUEST)



	body={
	'msg':'you are not administer!'
	}
	return Response(body,status=status.HTTP_403_FORBIDDEN)
