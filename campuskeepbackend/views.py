from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from .serializers import UserSerializer, ItemSerializer, MessageSerializer, ClaimSerializer
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.hashers import make_password
from .models import Item, Message, Claim
from django.contrib.auth.models import User
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from django.db.models import Q
import json
import jwt 
import datetime



#
# Creating new users 
#
@api_view(['POST'])
def create_user(request):
    try:
        # Assuming the data is sent as JSON
        data = json.loads(request.body)

        # Extracting user data
        username = data.get('username')
        email = data.get('email')
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        password = data.get('password')

        # Creating the user
        user = User.objects.create(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=make_password(password)  # Hash the password
        )

        return JsonResponse({'message': 'User created successfully'}, status=201)

    except Exception as e:
        return JsonResponse({'message': str(e)}, status=400)



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
        return JsonResponse({'username': user.username, 'email': user.email}, status=status.HTTP_200_OK)
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
def item_by_id(request, format=None):
    item_id = request.data.get('item_id')
    item = get_object_or_404(Item, pk=item_id)
    serializer = ItemSerializer(item)
    return Response(serializer.data)




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
def items_by_finder(request, format=None):

    if request.method == 'POST':
        # pull category field from incoming request 
        data = json.loads(request.body)
        found_by = data.get('found_by')
        items = Item.objects.filter(found_by=found_by)
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


#
# Gets a list of all conversations for a user 
#
@api_view(['POST'])
@csrf_exempt
def getConversationList(request, format=None):
    try:
        user_id = request.data.get('user')
        
        # Ensure user_id is provided and valid
        if not user_id:
            return JsonResponse({"error": "User ID is required."}, status=400)
        try:
            user_id = int(user_id)
            User.objects.get(pk=user_id)
        except (ValueError, User.DoesNotExist):
            return JsonResponse({"error": "Invalid User ID."}, status=400)

        # Query for messages where the user is either the sender or the receiver
        conversations = Message.objects.filter(Q(from_user_id=user_id) | Q(to_user_id=user_id))

        # Get unique user IDs
        user_ids = set()
        for message in conversations:
            user_ids.add(message.from_user_id)
            user_ids.add(message.to_user_id)

        # Remove the user's own ID from the set
        user_ids.discard(user_id)

        # Convert user IDs to list and return as JSON
        return JsonResponse({"users": list(user_ids)})
    except Exception as e:
        # Handle unexpected errors
        return JsonResponse({"error": str(e)}, status=500)



#
# Adding and Getting Claims
#
@api_view(['GET', 'POST', 'PUT'])
@csrf_exempt
def claim_list(request, format=None):

    # getting all claims
    if request.method == "GET":
        claims = Claim.objects.all()
        serializer = ClaimSerializer(claims, many=True)
        return Response(serializer.data)

    # storing new claims
    if request.method == "POST":
        serializer = ClaimSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return JsonResponse({"message": "Invalid payload"})

    # Updating an existing claim
    elif request.method == 'PUT':
        
        data = json.loads(request.body)
        claimId = data.get('id')

        try:
            claim = Claim.objects.get(id=claimId)
        except Claim.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = ClaimSerializer(claim, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#
# Endpoint for when claims are approved
#
@api_view(['POST'])
@csrf_exempt
def verifyClaim(request):
    try:
        claim_id = request.data.get('claim_id')
        
        # Ensure claim_id is provided
        if not claim_id:
            return JsonResponse({"error": "Claim ID is required."}, status=400)

        try:
            # Retrieve the claim and update its status
            claim = Claim.objects.get(pk=claim_id)
            claim.is_valid = True
            claim.save()

            # Update the associated item's status
            item = claim.item_id
            item.is_found = True
            item.save()

            return JsonResponse({"success": "Claim and Item status updated."})
        except ObjectDoesNotExist:
            return JsonResponse({"error": "Claim not found."}, status=404)
    except Exception as e:
        # Handle unexpected errors
        return JsonResponse({"error": str(e)}, status=500)
    


#
# Deleting a claim when it is denied by admin 
#
@api_view(['POST'])
@csrf_exempt
def denyClaim(request):
    try:
        claim_id = request.data.get('claim_id')
        
        # Ensure claim_id is provided
        if not claim_id:
            return JsonResponse({"error": "Claim ID is required."}, status=400)

        try:
            # Retrieve the claim
            claim = Claim.objects.get(pk=claim_id)

            # Delete the claim
            claim.delete()

            return JsonResponse({"success": "Claim successfully deleted."})
        except ObjectDoesNotExist:
            return JsonResponse({"error": "Claim not found."}, status=404)
    except Exception as e:
        # Handle unexpected errors
        return JsonResponse({"error": str(e)}, status=500)