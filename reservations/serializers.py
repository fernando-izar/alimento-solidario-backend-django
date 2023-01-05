from rest_framework import serializers
from .models import Reservations
from donations.serializers import DonationSerializer
from users.models import User
from users.serializers import UserSerializer
from rest_framework.validators import UniqueValidator
from donations.models import Donations
from django.forms import model_to_dict




class ReservationSerializer(serializers.ModelSerializer):
  
    user = UserSerializer(read_only = True)
    donation_id= serializers.UUIDField(
        required=True, validators=[UniqueValidator(queryset=Reservations.objects.all())])
    donation= DonationSerializer(read_only = True)
   
    class Meta:
        model = Reservations
        fields = ["id","date","donation_id", "user","donation"]
        depth = 2

    def get_donation(self, obj: Reservations):
        return model_to_dict(obj.donation)

class ReservationDetailSerializer(serializers.ModelSerializer):
     
    user = UserSerializer(read_only = True)
    donation = DonationSerializer(read_only = True)
    
    class Meta:
        model = Reservations
        fields = ["id", "date", "user", "donation_id", "donation"]
        depth = 2
        read_only_fields = ["donation_id"]

    def create(self,validated_data):
        reservation = Reservations.objects.create(**validated_data)
        reservation.save()
        return reservation
   
class ReservationDetailCreateSerializer(serializers.ModelSerializer):
  
    user = UserSerializer(read_only = True)
    donation_id= serializers.CharField(read_only = True)
   
    class Meta:
        model = Reservations
        fields = ["id","date","donation_id", "user","donation"]
        depth = 3

    def create(self,validated_data):
        reservation = Reservations.objects.create(**validated_data)
        reservation.save()
        return reservation    

    def get_donation(self, obj: Reservations):
        return model_to_dict(obj.donation)        

    ...
        


   

        

    