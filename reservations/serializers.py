from rest_framework import serializers
from .models import Reservations
from donations.serializers import DonationsSerializer
from users.models import User
from users.serializers import UserSerializer
from datetime import datetime



class ReservationSerializer(serializers.ModelSerializer):

    user = UserSerializer()
 
    class Meta:
        model = Reservations
        fields = ["id", "date", "donations", "user"]
        
        depth = 1


class ReservationDetailSerializer(serializers.ModelSerializer):
           
        
    user = UserSerializer()
    donation = DonationsSerializer()
 
    class Meta:
        model = Reservations
        fields = ["id", "date", "donation", "user"]
        
        depth = 2
   

        

    