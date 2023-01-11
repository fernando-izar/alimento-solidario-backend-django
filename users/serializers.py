from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import User, Type
from addresses.serializers import AddressSerializer
from addresses.models import Address
import pywhatkit
import pyautogui


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True, validators=[UniqueValidator(queryset=User.objects.all())]
    )
    cnpj_cpf = serializers.CharField(
        required=True, validators=[UniqueValidator(queryset=User.objects.all(), message="This field must be unique.")]
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
            "isActive",
            "address",
        )
        extra_kwargs = {"password": {"write_only": True}}
        methods = ["DELETE", "GET", "POST", "PUT", "PATCH"]

    def create(self, validated_data):
        address_data = validated_data.pop("address")
        address = Address.objects.create(**address_data)
        user = User.objects.create(address=address, **validated_data)
        user.set_password(validated_data["password"])
        user.save()

        contact = user.contact

        pywhatkit.sendwhatmsg_instantly(phone_no=contact, message="Bem vindo ao Alimento Solidário! Seu cadastro foi realizado com sucesso!")
        pyautogui.click()


        return user

    def update(self, instance, validated_data):
        address_data = validated_data.pop("address")
        address = instance.address
        for attr, value in address_data.items():
            setattr(address, attr, value)
        address.save()
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
