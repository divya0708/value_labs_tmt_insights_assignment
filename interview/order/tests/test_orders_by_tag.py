from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from interview.order.models import Order, OrderTag
from interview.inventory.models import Inventory, InventoryLanguage, InventoryType
from django.utils import timezone
from datetime import timedelta

class OrdersByTagListViewTest(APITestCase):
    def setUp(self):
        # Setup inventory
        inventory_type = InventoryType.objects.create(name="Book")
        language = InventoryLanguage.objects.create(name="English")
        inventory = Inventory.objects.create(name="Sample", type=inventory_type, language=language, metadata={})

        # Setup tags
        self.tag1 = OrderTag.objects.create(name="Urgent")
        self.tag2 = OrderTag.objects.create(name="Normal")

        # Setup orders
        self.order1 = Order.objects.create(
            inventory=inventory,
            start_date=timezone.now().date(),
            embargo_date=timezone.now().date() + timedelta(days=5),
            is_active=True,
        )
        self.order1.tags.add(self.tag1)

        self.order2 = Order.objects.create(
            inventory=inventory,
            start_date=timezone.now().date(),
            embargo_date=timezone.now().date() + timedelta(days=10),
            is_active=True,
        )
        self.order2.tags.add(self.tag2)

    def test_orders_filtered_by_tag(self):
        url = reverse('orders-by-tag-list', kwargs={'tag_id': self.tag1.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.json()
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['id'], self.order1.id)

    def test_orders_by_nonexistent_tag(self):
        url = reverse('orders-by-tag-list', kwargs={'tag_id': 9999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
