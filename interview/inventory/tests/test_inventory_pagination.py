from django.test import TestCase, Client
from django.urls import reverse
from interview.inventory.models import Inventory, InventoryLanguage, InventoryType

class InventoryListViewPaginationTest(TestCase):
    def setUp(self):
        self.client = Client()

        # Required related objects
        self.language = InventoryLanguage.objects.create(name="English")
        self.inventory_type = InventoryType.objects.create(name="Book")

        # Create 5 inventory items
        for i in range(5):
            Inventory.objects.create(
                name=f"Item {i+1}",
                metadata={
                    "language_id": self.language.id,
                    "tag_ids": [],
                    "type_id": self.inventory_type.id
                },
                language=self.language,
                type=self.inventory_type
            )

    def test_inventory_list_pagination_limit_3(self):
        response = self.client.get('/inventory/', {'limit': 3, 'offset': 0})
        self.assertEqual(response.status_code, 200)

        data = response.json()

        # Pagination structure
        self.assertIn('results', data)
        self.assertIn('count', data)
        self.assertIn('next', data)
        self.assertIn('previous', data)

        # Only 3 items returned
        self.assertEqual(len(data['results']), 3)
        self.assertEqual(data['count'], 5)
        self.assertIsNotNone(data['next'])
        self.assertIsNone(data['previous'])
