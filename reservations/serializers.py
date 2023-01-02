from rest_framework import serializers
from .models import Reservations
from donations.models import Donations
from users.models import User



class ReservationsSerializer(serializers.ModelSerializer):
    

    class Meta:
        model = Reservations
        fields = ["id", "date", "donation_id", "user_id"]