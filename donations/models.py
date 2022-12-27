from django.db import models
import uuid


class Donations(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    food = models.CharField(max_length=50)
    quantity = models.CharField(max_length=30)
    expiration_date = models.DateField()
    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    classification = models.ForeignKey(
        "classifications.Classification", on_delete=models.CASCADE
    )
