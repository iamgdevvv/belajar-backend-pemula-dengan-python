from rest_framework import serializers
from rest_framework.reverse import reverse

from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    _links = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "shop",
            "price",
            "sku",
            "description",
            "location",
            "discount",
            "category",
            "stock",
            "is_available",
            "picture",
            "is_delete",
            "_links",
        ]
        extra_kwargs = {
            "picture": {"allow_blank": True, "required": False},
            "is_delete": {"required": False},
        }

    def get__links(self, obj: Product):
        request = self.context.get("request")

        products_href = reverse("products-list", request=request)
        detail_href = reverse("products-detail", kwargs={"pk": str(obj.pk)}, request=request)

        return [
            {"rel": "self", "href": products_href, "action": "POST", "types": ["application/json"]},
            {"rel": "self", "href": detail_href, "action": "GET", "types": ["application/json"]},
            {"rel": "self", "href": detail_href, "action": "PUT", "types": ["application/json"]},
            {"rel": "self", "href": detail_href, "action": "DELETE", "types": ["application/json"]},
        ]

    def create(self, validated_data):
        product = super().create(validated_data)

        if "is_delete" in getattr(self, "initial_data", {}):
            product.supports_soft_delete = True
            product.save(update_fields=["supports_soft_delete"])

        return product

    def update(self, instance, validated_data):
        product = super().update(instance, validated_data)

        if "is_delete" in getattr(self, "initial_data", {}) and not product.supports_soft_delete:
            product.supports_soft_delete = True
            product.save(update_fields=["supports_soft_delete"])

        return product
