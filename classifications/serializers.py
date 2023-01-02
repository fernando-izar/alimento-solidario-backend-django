from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import Classification


class ClassificationSerializer(serializers.ModelSerializer):
    name = serializers.CharField(
        required=True, validators=[UniqueValidator(queryset=Classification.objects.all())]
    )

    class Meta:
        model = Classification
        fields = ("id", "name",)
        extra_kwargs = {"id": {"read_only": True}}

    def create(self, validated_data):
        classification = Classification.objects.create(**validated_data)
        classification.save()
        return classification

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance