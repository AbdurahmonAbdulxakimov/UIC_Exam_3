from rest_framework import serializers

from products import models


class MaterialSerializer(serializers.Serializer):
    name = serializers.CharField()
    quantity = serializers.FloatField()


class ProductMaterialsNeededSerializer(serializers.Serializer):
    name = serializers.CharField()
    quantity = serializers.IntegerField()
    required_materials = MaterialSerializer(many=True)
