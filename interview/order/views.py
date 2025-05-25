from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response

from interview.order.models import Order, OrderTag
from interview.order.serializers import OrderSerializer, OrderTagSerializer

# Create your views here.
class OrderListCreateView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    

class OrderTagListCreateView(generics.ListCreateAPIView):
    queryset = OrderTag.objects.all()
    serializer_class = OrderTagSerializer


class DeactivateOrderView(APIView):
    def post(self, request, pk):
        order = get_object_or_404(Order, pk=pk)

        if not order.is_active:
            return Response(
                {"detail": "Order is already inactive."},
                status=status.HTTP_400_BAD_REQUEST
            )

        order.is_active = False
        order.save()

        return Response(
            {"detail": "Order deactivated successfully."},
            status=status.HTTP_200_OK
        )
