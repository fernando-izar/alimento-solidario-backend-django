from rest_framework import serializers
from .models import Reservations
from donations.serializers import DonationSerializer
from users.models import User
from users.serializers import UserSerializer
from rest_framework.validators import UniqueValidator
from donations.models import Donations




class ReservationSerializer(serializers.ModelSerializer):
    donation = serializers.PrimaryKeyRelatedField(read_only=True)
    user = UserSerializer(read_only = True)
    class Meta:
        model = Reservations
        fields = ["id","date","donation", "user"]
     
        depth = 1


class ReservationDetailSerializer(serializers.ModelSerializer):
     
    user = UserSerializer(read_only = True)
    donation = DonationSerializer()
 
    class Meta:
        model = Reservations
        fields = ["id", "date", "donation", "user"]
        
        depth = 2



   

        

    