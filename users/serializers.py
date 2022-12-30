from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import User, Type
from addresses.serializers import AddressSerializer


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True, validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(min_length=4, write_only=True)
    name = serializers.CharField(required=True)
    cnpj_cpf = serializers.CharField(
        required=True, validators=[UniqueValidator(queryset=User.objects.all())]
    )
    responsible = serializers.CharField(required=True)
    contact = serializers.CharField(required=True)
    type = serializers.ChoiceField(choices=Type.choices, default=Type.DEFAULT)
    isAdm = serializers.BooleanField(default=False)
    address = AddressSerializer(required=True)

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
