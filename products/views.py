from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Product
from .serializers import ProductSerializer


class ProductListCreateAPIView(APIView):
    def get(self, request):
        queryset = Product.objects.filter(is_delete=False)

        name = request.query_params.get("name")
        if name:
            queryset = queryset.filter(name__icontains=name)

        location = request.query_params.get("location")
        if location:
            queryset = queryset.filter(location__icontains=location)

        serializer = ProductSerializer(queryset, many=True, context={"request": request})
        return Response({"products": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ProductSerializer(data=request.data, context={"request": request})
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        product = serializer.save()
        output = ProductSerializer(product, context={"request": request}).data
        return Response(output, status=status.HTTP_201_CREATED)


class ProductDetailAPIView(APIView):
    def _get_object(self, pk):
        try:
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist as exc:
            raise NotFound() from exc

    def get(self, request, pk):
        product = self._get_object(pk)
        serializer = ProductSerializer(product, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        product = self._get_object(pk)

        serializer = ProductSerializer(product, data=request.data, context={"request": request})
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        product = self._get_object(pk)
        if product.supports_soft_delete:
            product.is_delete = True
            product.save(update_fields=["is_delete"])
        else:
            product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
