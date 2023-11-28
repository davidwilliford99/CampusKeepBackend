from rest_framework import serializers
from .models import *

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['id', 'name', 'category', 'description','question1', 'answer1', 'question2', 'answer2', 'question3', 'answer3', 'found_by', 'is_found']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'password', 'is_staff']

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'from_user', 'to_user', 'content', 'time_sent']

class ClaimSerializer(serializers.ModelSerializer):
    class Meta:
        model = Claim
        fields = ['id', 'claimed_by', 'finder', 'claim_date', 'item_id', 'answer1', 'answer2', 'answer3', 'is_valid']