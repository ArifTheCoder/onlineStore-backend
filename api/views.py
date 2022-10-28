import io
from django.shortcuts import render
from rest_framework import mixins
from rest_framework import filters
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ReadOnlyModelViewSet
from PIL import Image
from django.http import Http404
from rest_framework import status
from rest_framework.exceptions import PermissionDenied, ParseError
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Product

from .serializers import ProductSerializer

PRODUCT_IMAGE_MAXIMUM_HEIGHT = 650


class ProductViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
):
    search_fields = ['name', 'brand', 'description', 'price']
    filter_backends = (filters.SearchFilter,)
    serializer_class = ProductSerializer

    def get_queryset(self):
        return Product.objects.all().order_by("-created_at")


class ProductImageUploadView(APIView):

    parser_class = (FileUploadParser,)

    def post(self, request, product_id):
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            raise Http404

        image_file = request.FILES.get("image")
        if not image_file:
            raise ParseError(("Missing image."))

        try:
            image = Image.open(image_file)
        except OSError:
            raise ParseError(("The file needs to be an image file."))

        if image.format not in ("JPEG", "PNG"):
            raise ParseError(("Only .jpg or .png images are supported."))

        width, height = image.size
        if width > PRODUCT_IMAGE_MAXIMUM_HEIGHT:
            image.thumbnail(
                size=(PRODUCT_IMAGE_MAXIMUM_HEIGHT,
                      PRODUCT_IMAGE_MAXIMUM_HEIGHT)
            )
            image_file = io.BytesIO()
            image.save(fp=image_file, format=image.format)

        product.image.save(
            name="%s.%s" % (product.pk, "jpg" if image.format ==
                            "JPEG" else "png"),
            content=image_file,
            save=True,
        )

        return Response(status=status.HTTP_201_CREATED)
