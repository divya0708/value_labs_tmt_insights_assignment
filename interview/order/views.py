from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from django.utils.dateparse import parse_date

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


class OrderDateRangeListView(generics.ListAPIView):
    serializer_class = OrderSerializer

    def get_queryset(self):
        start_date_str = self.request.query_params.get("start_date")
        embargo_date_str = self.request.query_params.get("embargo_date")

        if not start_date_str or not embargo_date_str:
            raise ValidationError("start_date and embargo_date query parameters are required")
        
        start_date = parse_date(start_date_str)
        embargo_date = parse_date(embargo_date_str)

        if not start_date or not embargo_date:
            raise ValidationError("Invalid date format. Use YYYY-MM-DD")
        
        # Filter orders where start_date >= provided start_date AND embargo_date <= provided embargo_date
        return Order.objects.filter(start_date__gte=start_date, embargo_date__lte=embargo_date)
    

class OrdersByTagListView(generics.ListAPIView):
    serializer_class = OrderSerializer

    def get_queryset(self):
        tag_id = self.kwargs.get('tag_id')
        tag = get_object_or_404(OrderTag, pk=tag_id)
        return tag.orders.all()
