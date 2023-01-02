from rest_framework import serializers
from .models import Donations
from users.models import User
from users.serializers import UserSerializer

class DonationSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

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
        "user",
        ]
        depth=1

        

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
        depth=1