from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import Address


class AddressSerializer(serializers.ModelSerializer):
    address = serializers.CharField(required=True)
    complement = serializers.CharField(required=True)
    city = serializers.CharField(required=True)
    state = serializers.CharField(required=True)
    zipCode = serializers.CharField(required=True)

    class Meta:
        model = Address
        fields = (
            "id",
            "address",
            "complement",
            "city",
            "state",
            "zipCode",
        )
