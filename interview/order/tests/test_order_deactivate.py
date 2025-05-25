from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

from interview.inventory.models import Inventory, InventoryType, InventoryLanguage
from interview.order.models import Order, OrderTag
from django.utils import timezone
from datetime import timedelta


class DeactivateOrderViewTests(APITestCase):
    def setUp(self):
        # Create dependencies for Inventory and Order
        inventory_type = InventoryType.objects.create(name="Type1")
        inventory_language = InventoryLanguage.objects.create(name="English")
        inventory = Inventory.objects.create(
            name="Test Inventory",
            type=inventory_type,
            language=inventory_language,
            metadata={"year": 2022}
        )
        tag = OrderTag.objects.create(name="Test Tag")

        self.order = Order.objects.create(
            inventory=inventory,
            start_date=timezone.now().date(),
            embargo_date=(timezone.now() + timedelta(days=30)).date()
        )
        self.order.tags.add(tag)

        self.deactivate_url = reverse('order-deactivate', args=[self.order.id])

    def test_deactivate_active_order(self):
        response = self.client.post(self.deactivate_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['detail'], 'Order deactivated successfully.')

        # Verify from DB
        self.order.refresh_from_db()
        self.assertFalse(self.order.is_active)

    def test_deactivate_already_inactive_order(self):
        # Manually deactivate
        self.order.is_active = False
        self.order.save()

        response = self.client.post(self.deactivate_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()['detail'], 'Order is already inactive.')

    def test_deactivate_non_existent_order(self):
        invalid_url = reverse('order-deactivate', args=[9999])
        response = self.client.post(invalid_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
