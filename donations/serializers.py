from rest_framework import serializers
from .models import Donations
from users.models import User
from users.serializers import UserSerializer
from classifications.serializers import ClassificationSerializer
from rest_framework.validators import UniqueValidator
from .models import Donations
from django.forms import model_to_dict

class DonationSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    classification = ClassificationSerializer(read_only = True)
    classification_id= serializers.UUIDField(
        required=True, write_only=True)
    
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
        "classification_id",
        "user",
        ]             
        depth=2

    def get_donation(self, obj: Donations):
        return model_to_dict(obj.classification)
        

class DonationDetailSerializer(serializers.ModelSerializer):
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


class DonationUserSerializer(serializers.ModelSerializer):
    donations = DonationSerializer(many=True)
    
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


class DonationExpandSerializer(serializers.ModelSerializer):
    user = UserSerializer()

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
        read_only_fields=['user']
        depth=1


class DonationExpandDetailSerializer(serializers.ModelSerializer):
    user = UserSerializer()

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
        depth=1