from django.db import models

from utils.models import BaseModel


class Product(BaseModel):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return f"{self.code}"


class Material(BaseModel):
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name}"


class ProductMaterial(BaseModel):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="product_material"
    )
    material = models.ForeignKey(
        Material, on_delete=models.CASCADE, related_name="product_material"
    )

    quantity = models.FloatField()


class Warehouse(BaseModel):
    material = models.ForeignKey(
        Material, on_delete=models.CASCADE, related_name="warehouse"
    )
    remainder = models.PositiveBigIntegerField()
    price = models.DecimalField(decimal_places=2, max_digits=15)
