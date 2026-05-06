from django.urls import path

from .views import ProductDetailAPIView, ProductListCreateAPIView

urlpatterns = [
    path("products/", ProductListCreateAPIView.as_view(), name="products-list"),
    path("products", ProductListCreateAPIView.as_view()),
    path("products/<uuid:pk>/", ProductDetailAPIView.as_view(), name="products-detail"),
    path("products/<uuid:pk>", ProductDetailAPIView.as_view()),
]

