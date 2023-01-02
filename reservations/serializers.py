from rest_framework import serializers
from .models import Reservations
from donations.serializers import DonationsSerializer
from users.models import User
from users.serializers import UserSerializer
from datetime import datetime



class ReservationsSerializer(serializers.ModelSerializer):

 
    class Meta:
        model = Reservations
        fields = ["id", "date", "donation", "user"]

        read_only_fields = ['user']
        
        depth = 1

   

        

    