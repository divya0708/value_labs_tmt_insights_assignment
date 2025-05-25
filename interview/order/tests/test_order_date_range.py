from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.utils import timezone
from datetime import timedelta

from interview.order.models import Order, OrderTag
from interview.inventory.models import Inventory, InventoryLanguage, InventoryTag, InventoryType


class OrderDateRangeListViewTests(APITestCase):
    from interview.order.models import OrderTag

class OrderDateRangeListViewTests(APITestCase):
    def setUp(self):
        # Setup related models
        self.type = InventoryType.objects.create(name="Type1")
        self.language = InventoryLanguage.objects.create(name="English")
        self.tag = OrderTag.objects.create(name="Tag1")  # <-- Use OrderTag here

        # Inventories
        self.inventory1 = Inventory.objects.create(
            name="Inventory1",
            type=self.type,
            language=self.language,
            metadata={"year": 2020}
        )
        self.inventory2 = Inventory.objects.create(
            name="Inventory2",
            type=self.type,
            language=self.language,
            metadata={"year": 2024}
        )

        # Orders with different start_date and embargo_date
        self.order1 = Order.objects.create(
            inventory=self.inventory1,
            start_date=timezone.now().date() - timedelta(days=10),
            embargo_date=timezone.now().date() - timedelta(days=5),
            is_active=True,
        )
        self.order1.tags.add(self.tag)

        self.order2 = Order.objects.create(
            inventory=self.inventory2,
            start_date=timezone.now().date() - timedelta(days=3),
            embargo_date=timezone.now().date() + timedelta(days=2),
            is_active=True,
        )
        self.order2.tags.add(self.tag)

    def test_orders_filtered_by_date_range(self):
        url = reverse('order-date-range-list')
        start_date = (timezone.now().date() - timedelta(days=4)).isoformat()
        embargo_date = (timezone.now().date() + timedelta(days=3)).isoformat()

        response = self.client.get(url, {'start_date': start_date, 'embargo_date': embargo_date})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        results = response.json()
        # Should only contain order2, because order1 start_date is before start_date filter
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['id'], self.order2.id)

    def test_missing_query_params(self):
        url = reverse('order-date-range-list')
        response = self.client.get(url)  # no params

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('start_date and embargo_date query parameters are required', str(response.data))

    def test_invalid_date_format(self):
        url = reverse('order-date-range-list')
        response = self.client.get(url, {'start_date': 'invalid', 'embargo_date': 'also-invalid'})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Invalid date format. Use YYYY-MM-DD', str(response.data))
