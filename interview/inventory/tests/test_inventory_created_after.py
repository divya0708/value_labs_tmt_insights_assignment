from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.utils import timezone
from datetime import timedelta
from interview.inventory.models import Inventory, InventoryLanguage, InventoryTag, InventoryType

class InventoryCreatedAfterListViewTests(APITestCase):
    def setUp(self):
        # Create related models required for Inventory
        self.type = InventoryType.objects.create(name="Type1")
        self.language = InventoryLanguage.objects.create(name="English")
        self.tag = InventoryTag.objects.create(name="Tag1")

        # Create inventory items at different created_at times
        self.old_inventory = Inventory.objects.create(
            name="Old Inventory",
            type=self.type,
            language=self.language,
            metadata={"year": 2020, "actors": ["A"], "imdb_rating": 7.5, "rotten_tomatoes_rating": 80}
        )
        self.old_inventory.tags.add(self.tag)
        self.old_inventory.created_at = timezone.now() - timedelta(days=10)
        self.old_inventory.save()

        self.new_inventory = Inventory.objects.create(
            name="New Inventory",
            type=self.type,
            language=self.language,
            metadata={"year": 2024, "actors": ["B"], "imdb_rating": 8.3, "rotten_tomatoes_rating": 90}
        )
        self.new_inventory.tags.add(self.tag)
        self.new_inventory.created_at = timezone.now() - timedelta(days=1)
        self.new_inventory.save()

    def test_inventory_created_after_filter(self):
        url = reverse('inventory-created-after-list')
        filter_date = (timezone.now() - timedelta(days=5)).isoformat()
        response = self.client.get(url, {'created_after': filter_date})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.json()
        #Should only contain new inventory
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['name'], 'New Inventory')

    def test_missing_created_after_param(self):
        url= reverse('inventory-created-after-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.json())

    def test_invalid_created_after_param(self):
        url = reverse('inventory-created-after-list')
        response = self.client.get(url, {'created_after': 'invalid-date'})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.json())