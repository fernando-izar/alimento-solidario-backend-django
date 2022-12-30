from django.db import models
from django.contrib.auth.models import AbstractUser, AbstractBaseUser, BaseUserManager
import uuid


class Type(models.TextChoices):
    DONNOR = "donor"
    CHARITY = "charity"
    DEFAULT = "Not Informed"


class CustomUserManager(BaseUserManager):
    def get_by_natural_key(self, email):
        return self.get(email=email)

class User(AbstractBaseUser):

    email = models.EmailField(unique=True, null=False)
    objects = CustomUserManager()
    USERNAME_FIELD = "email"
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    password = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    cnpj_cpf = models.CharField(max_length=18, unique=True)
    responsible = models.CharField(max_length=100)
    contact = models.CharField(max_length=50)
    type = models.CharField(max_length=12, choices=Type.choices, default=Type.DEFAULT)
    isAdm = models.BooleanField(default=False)
    address = models.OneToOneField("addresses.Address", on_delete=models.CASCADE)
    