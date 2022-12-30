from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import User, Type
from addresses.serializers import AddressSerializer
from addresses.models import Address


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True, validators=[UniqueValidator(queryset=User.objects.all())]
    )
    cnpj_cpf = serializers.CharField(
        required=True, validators=[UniqueValidator(queryset=User.objects.all())]
    )
    type = serializers.ChoiceField(choices=Type.choices, default=Type.DEFAULT)
    address = AddressSerializer()

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "password",
            "name",
            "cnpj_cpf",
            "responsible",
            "contact",
            "type",
            "isAdm",
            "address",
        )
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        address_data = validated_data.pop("address")
        address = Address.objects.create(**address_data)
        user = User.objects.create(address=address, **validated_data)
        return user
