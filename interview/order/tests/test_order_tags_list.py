from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from interview.order.models import Order, OrderTag
from interview.inventory.models import Inventory, InventoryLanguage, InventoryType
from django.utils import timezone
from datetime import timedelta

class OrderTagsListViewTest(APITestCase):
    def setUp(self):
        # Create Inventory related models
        self.inventory_type = InventoryType.objects.create(name="Book")
        self.language = InventoryLanguage.objects.create(name="English")

        # Create some OrderTags
        self.tag1 = OrderTag.objects.create(name="Urgent")
        self.tag2 = OrderTag.objects.create(name="Gift")

        # Create Inventory instance
        self.inventory = Inventory.objects.create(
            name="Sample Inventory",
            type=self.inventory_type,
            language=self.language,
            metadata={"info": "sample"}
        )

        # Create Orders and assign tags
        self.order1 = Order.objects.create(
            inventory=self.inventory,
            start_date=timezone.now().date(),
            embargo_date=timezone.now().date() + timedelta(days=5),
            is_active=True,
        )
        self.order1.tags.add(self.tag1)

        self.order2 = Order.objects.create(
            inventory=self.inventory,
            start_date=timezone.now().date(),
            embargo_date=timezone.now().date() + timedelta(days=10),
            is_active=True,
        )
        self.order2.tags.add(self.tag2)

    def test_list_order_tags(self):
        url = reverse('order-tags-list', kwargs={'pk': self.order1.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        tags = response.json()
        tag_names = [tag['name'] for tag in tags]
        self.assertIn(self.tag1.name, tag_names)
        self.assertNotIn(self.tag2.name, tag_names)

        # Also check order2 tags
        url = reverse('order-tags-list', kwargs={'pk': self.order2.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        tags = response.json()
        tag_names = [tag['name'] for tag in tags]
        self.assertIn(self.tag2.name, tag_names)
        self.assertNotIn(self.tag1.name, tag_names)

    def test_list_order_tags_no_tags(self):
        self.order1.tags.clear()
        self.order2.tags.clear()

        url = reverse('order-tags-list', kwargs={'pk': self.order1.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), [])

        url = reverse('order-tags-list', kwargs={'pk': self.order2.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), [])
