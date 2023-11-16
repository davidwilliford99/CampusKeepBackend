from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from .serializers import UserSerializer, ItemSerializer, MessageSerializer
from .models import Item, Message, Claim
from django.contrib.auth.models import User
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.db.models import Q
import json
import jwt 
import datetime



#
# Creating new users 
#
@api_view(['POST'])
def create_user(request):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():

            username = serializer.validated_data['username']
            email = serializer.validated_data['email']

            # checking for duplicate usernames and emails
            if User.objects.filter(username=username).exists():
                return Response({'error': 'Username is already taken.'}, status=status.HTTP_400_BAD_REQUEST)
            elif User.objects.filter(email=email).exists():
                return Response({'error': 'Email is already in use.'}, status=status.HTTP_400_BAD_REQUEST)

            else:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response({'error': 'Bad Payload'}, status=status.HTTP_400_BAD_REQUEST)



#
# Logs in user 
#
@api_view(['POST'])
@csrf_exempt
def loginUser(request):
    if request.method == 'POST':
        
        data = json.loads(request.body)
        email = data.get('email')
        password = data.get('password')
        
        print(email + " " + password)
        user = User.objects.filter(email=email).first()
        
        if user is None:
            return JsonResponse({'message': 'Invalid email'})
        if not user.check_password(password):
            return JsonResponse({'message': 'Incorrect Password'})

        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=120),
            'iat': datetime.datetime.utcnow()
        }
        token = jwt.encode(payload, 'BGCcret', algorithm='HS256')  # second param is secret key for hashing
    
        # if succesful
        print("Login Successful")
        return JsonResponse({'jwt': token})
            
    else:
        return JsonResponse({'message': 'Invalid authentication request'}, status=405)




#
# Gets user info using jwt
#
@api_view(['POST'])
@csrf_exempt
def userInfo(request):
    
    if request.method == 'POST':
    
        data = json.loads(request.body)
        token = data.get('jwt')

        if not token:
            return JsonResponse({'message': 'You are not signed in'}) 
        try:
            payload = jwt.decode(token, 'BGCcret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return JsonResponse({'message': 'Invalid web token'}) 

        user = User.objects.filter(id=payload['id']).first()
        user_serializer = UserSerializer(user)
        
        return Response(user_serializer.data) 



@api_view(['POST'])
@csrf_exempt
def getUsername(request):

    user_id = request.data.get('user_id')
    if not user_id:
        return JsonResponse({'error': 'User ID is required'}, status=status.HTTP_400_BAD_REQUEST)
    try:
        user = User.objects.get(pk=user_id)
        return JsonResponse({'username': user.username}, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)




@api_view(['GET', 'POST'])
@csrf_exempt
def item_list(request, format=None):

    # getting all Items
    if request.method == "GET":
        grafts = Item.objects.all()
        serializer = ItemSerializer(grafts, many=True)
        return Response(serializer.data)

    # storing new Items
    if request.method == "POST":
        serializer = ItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return JsonResponse({"message": "Invalid payload"})
    


@api_view(['POST'])
@csrf_exempt
def items_by_category(request, format=None):

    if request.method == 'POST':
        # pull category field from incoming request 
        data = json.loads(request.body)
        categoryInput = data.get('category')
        items = Item.objects.filter(category=categoryInput)
        serializer = ItemSerializer(items, many=True)
        return Response(serializer.data)



@api_view(['POST'])
@csrf_exempt
def newMessage(request, format=None):
    serializer = MessageSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
@csrf_exempt
def getMessages(request, format=None):
    if request.method == 'POST':
        data = json.loads(request.body)
        userId = data.get('user_id')

        # find messages to and from the userID
        # Order by 'time_sent' in descending order
        messages = Message.objects.filter(
            Q(from_user_id=userId) | Q(to_user_id=userId)
        ).order_by('-time_sent')  

        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)



#
# Gets a conversation between 2 users
#
@api_view(['POST'])
@csrf_exempt
def getConversation(request, format=None):
    from_user = request.data.get('from_user')
    to_user = request.data.get('to_user')

    if not all([from_user, to_user]):
        return Response({"error": "Both user IDs are required."}, status=status.HTTP_400_BAD_REQUEST)

    messages = Message.objects.filter(
        Q(from_user=from_user, to_user=to_user) |
        Q(from_user=to_user, to_user=from_user)
    ).order_by('time_sent')

    serializer = MessageSerializer(messages, many=True)
    return Response(serializer.data)