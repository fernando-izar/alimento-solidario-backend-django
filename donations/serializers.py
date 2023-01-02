from rest_framework import serializers
from .models import Donations
from users.models import User

class DonationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Donations
        fields = [
        "id", 
        "food", 
        "quantity", 
        "expiration", 
        "available", 
        "createdAt", 
        "updatedAt", 
        "classification",
        ]
        extra_kwargs = {"createdAt": {"auto_now_add": True}, "updatedAt": {"auto_now": True}}

class DonationExpandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Donations
        fields = [
        "id", 
        "food", 
        "quantity", 
        "expiration", 
        "available", 
        "createdAt", 
        "updatedAt", 
        "user",
        "classification",
        ]

class DonationFromUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
        "id", 
        "email", 
        "name", 
        "responsible", 
        "contact", 
        "type", 
        "isAdm", 
        "isActive",
        "donations",
        "address",
        ]