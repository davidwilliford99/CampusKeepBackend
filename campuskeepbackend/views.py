from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from .serializers import UserSerializer, ItemSerializer
from .models import Item, Message, Claim
from django.contrib.auth.models import User
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
import json
import jwt 
import datetime





#
# Logs in user 
#
# Checks for valid email and password, and returns jwt
# Session automatically expires after 2 hours
#
@api_view(['POST'])
@csrf_exempt
def loginUser(request):
    if request.method == 'POST':
        
        # Get the request data as a dictionary
        data = json.loads(request.body)
        email = data.get('email')
        password = data.get('password')
        
        print(email + " " + password)

        # find user by email in request payload
        user = User.objects.filter(email=email).first()
        
        # if user not found
        if user is None:
            return JsonResponse({'message': 'Invalid email'})
        
        # checking password match, check_passwords checks hashed passwords
        if not user.check_password(password):
            return JsonResponse({'message': 'Incorrect Password'})
        
        # creating jwt token
        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=120),
            'iat': datetime.datetime.utcnow()
        }
        token = jwt.encode(payload, 'BGCcret', algorithm='HS256')  # second param is secret key for hashing
    
        
        # if succesful login 
        print("Login Successful")
        
        # returning jwt token
        # frontend will store token into localstorage
        return JsonResponse({'jwt': token})
        
            
    else:
        return JsonResponse({'message': 'Invalid authentication request'}, status=405)




#
# User sends their jwt 
#
# Response contains all of their user info
#
@api_view(['POST'])
@csrf_exempt
def userInfo(request):
    
    if request.method == 'POST':
    
        # pull token from cookies 
        data = json.loads(request.body)
        token = data.get('jwt')
        
        # checks for jwt token (credentials)
        if not token:
            return JsonResponse({'message': 'You are not signed in'}) 

        # decode jwt
        try:
            payload = jwt.decode(token, 'BGCcret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return JsonResponse({'message': 'Invalid web token'}) 
        
        # get user data and profile data using id within token
        user = User.objects.filter(id=payload['id']).first()
        user_serializer = UserSerializer(user)
        
        return Response(user_serializer.data) 



#
# Gets all Items (all fields)
#
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
        
