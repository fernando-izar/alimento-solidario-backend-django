from rest_framework import serializers
from .models import Reservations
from donations.serializers import DonationSerializer
from users.models import User
from users.serializers import UserSerializer
from rest_framework.validators import UniqueValidator
from donations.models import Donations




class ReservationSerializer(serializers.ModelSerializer):
    

    donation_id = serializers.CharField(
        required=True, validators=[UniqueValidator(queryset=Reservations.objects.all())]
    )


    user = UserSerializer(read_only = True)
    class Meta:
        model = Reservations
        fields = ["id","date","donation_id", "user"]
     
        depth = 1


class ReservationDetailSerializer(serializers.ModelSerializer):
     
    user = UserSerializer(read_only = True)
    donation = DonationSerializer()
 
    class Meta:
        model = Reservations
        fields = ["id", "date", "donation_id", "user"]
        
        depth = 2



   

        

    