from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid


class Type(models.TextChoices):
    DONNOR = "donor"
    CHARITY = "charity"
    DEFAULT = "Not Informed"


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    cnpj_cpf = models.CharField(max_length=18)
    responsible = models.CharField(max_length=100)
    contact = models.CharField(max_length=50)
    type = models.CharField(max_length=10, choices=Type.choices, default=Type.DEFAULT)
    isAdm = models.BooleanField(default=False)
    address = models.OneToOneField("addresses.Address", on_delete=models.CASCADE)
