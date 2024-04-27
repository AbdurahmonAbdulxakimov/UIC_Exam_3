from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Subquery, OuterRef, F, Value
from django.db.models.functions import JSONObject
from django.contrib.postgres.expressions import ArraySubquery

from products import models, serializers


class ResultView(APIView):
    def post(self, request, *args, **kwargs):
        code = request.data.get("code")
        quantity = float(request.data.get("quantity"))

        qs = models.Product.objects.filter(code=code).annotate(
            quantity=Value(quantity),
            required_materials=ArraySubquery(
                models.ProductMaterial.objects.filter(product_id=OuterRef("id"))
                .annotate(
                    total_quantity=F("quantity") * quantity,
                    json=JSONObject(
                        name="material__name",
                        quantity="total_quantity",
                    ),
                )
                .values("json")
            ),
        )

        serializer = serializers.ProductMaterialsNeededSerializer(qs, many=True)

        # Determine from which warehouses we can obtain the required quantities of each material
        warehouses = (
            models.Warehouse.objects.select_related("material")
            .all()
            .annotate(material_name=F("material__name"))
            .values()
        )
        result = []

        for product in serializer.data:
            product_materials = []
            for material in product.get("required_materials"):
                material_name = material.get("name")
                required_qty = int(material.get("quantity"))
                remaining_qty = int(required_qty)

                for warehouse in warehouses:
                    if remaining_qty <= 0:
                        break
                    if warehouse.get("material_name") != material_name:
                        continue

                    qty_to_take = min(warehouse.get("remainder"), remaining_qty)
                    product_materials.append(
                        {
                            "warehouse_id": warehouse.get("id"),
                            "material_name": material_name,
                            "qty": qty_to_take,
                            "price": warehouse.get("price"),
                        }
                    )
                    remaining_qty -= qty_to_take

                if remaining_qty > 0:
                    product_materials.append(
                        {
                            "warehouse_id": None,
                            "material_name": material_name,
                            "qty": remaining_qty,
                            "price": None,
                        }
                    )

            result.append(
                {
                    "product_name": product.get("name"),
                    "product_qty": product.get("quantity"),
                    "product_materials": product_materials,
                }
            )

        # return Response(status=status.HTTP_200_OK, data=serializer.data)
        return Response(status=status.HTTP_200_OK, data={"result": result})
