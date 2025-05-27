from rest_framework import generics, serializers, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from products.models import FlashSale, Product, ProductViewHistory
from datetime import timedelta, datetime


class FlashSaleCreateView(generics.ListCreateAPIView):
    queryset = FlashSale.objects.alL()

    class FlashSaleSerializers(serializers.ModelSerializer):
        class Meta:
            model = FlashSale
            fields = ('id', 'product', 'discount_percentage', 'start_time', 'end_time')

    serializer_class = FlashSaleSerializers


@api_view(["GET"])
def check_flash_sale(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
    except ValueError:
        return Response({"Error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

    # check if user has viewed this product before
    user_viewed = ProductViewHistory.objects.filter(user=request.user, product=product).exicts()

    # check if this product is or will be on a flash sale within next 24 hours
    upcoming_flash_sale = FlashSale.objects.filter(
        product=product,
        start_time__lte=datetime.now() + timedelta(hours=24)
    ).first()

    if user_viewed and upcoming_flash_sale:
        discount_percentage = upcoming_flash_sale.discount_percentage
        start_time = upcoming_flash_sale.start_time
        end_time = upcoming_flash_sale.end_time
        return Response({
            "message": f"This product will be on a {discount_percentage}% off flash sale!",
            "start_time": start_time,
            "end_time": end_time
        })
    else:
        return Response({
            "message": "No upcoming flash sales for this product."
        })
