from rest_framework.routers import DefaultRouter
from django.urls import path

from .views import ProductImageUploadView, ProductViewSet

router = DefaultRouter()
router.register('products', ProductViewSet, basename='products')

app_name = "api"
urlpatterns = router.urls + [
    path(
        "product-image/<str:product_id>/",
        ProductImageUploadView.as_view(),
        name="product-image-upload",
    ),
]
