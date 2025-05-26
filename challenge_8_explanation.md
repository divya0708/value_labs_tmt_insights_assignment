# Challenge 8: Adding an Inventory Item through the API with Metadata

## Objective

You need to allow adding a new Inventory item through the API with rich metadata. The metadata must include these fields:

- year (integer)
- actors (list of strings)
- imdb_rating (float)
- rotten_tomatoes_rating (integer)
- film_locations (list of strings)

---

## What You Need to Do

1. **Ensure the view supports POST requests**  
   The `InventoryListCreateView` already has a `post` method that:
   - Validates and parses the `metadata` field using a Pydantic schema.
   - Validates the entire request data using the `InventorySerializer`.
   - Saves the new Inventory item if validation passes.

2. **Modify the Serializer to support POST**  
   The existing `InventorySerializer` may have nested serializers for related fields (`type`, `language`, `tags`) that work fine for GET but cause issues for POST.

   To fix this, change those related fields to use `PrimaryKeyRelatedField` with appropriate `queryset` parameters, so that when posting, the API expects just IDs instead of nested objects.

   Example:

   ```python
   from rest_framework import serializers
   from interview.inventory.models import Inventory, InventoryType, InventoryLanguage, InventoryTag

   class InventorySerializer(serializers.ModelSerializer):
       type = serializers.PrimaryKeyRelatedField(queryset=InventoryType.objects.all())
       language = serializers.PrimaryKeyRelatedField(queryset=InventoryLanguage.objects.all())
       tags = serializers.PrimaryKeyRelatedField(queryset=InventoryTag.objects.all(), many=True)
       metadata = serializers.JSONField()

       class Meta:
           model = Inventory
           fields = ['id', 'name', 'type', 'language', 'tags', 'metadata']
   ```

3. **Format your POST request data correctly**

   Your JSON payload to create a new inventory item should look like this:

   ```json
   {
     "name": "Interstellar",
     "type": 2,
     "language": 1,
     "tags": [1, 3],
     "metadata": {
       "year": 2014,
       "actors": ["Matthew McConaughey", "Anne Hathaway"],
       "imdb_rating": 8.6,
       "rotten_tomatoes_rating": 72,
       "film_locations": ["Iceland", "Canada"]
     }
   }
   ```

4. **Test your API**

   Send the above payload to the Inventory POST endpoint.  
   If everything is set up correctly:
   - The metadata will be validated via the Pydantic schema inside the view.
   - The serializer will validate related fields by their IDs.
   - The new Inventory item will be saved and returned with HTTP 201 status.

---

## Summary

- The view already supports POST with metadata parsing.
- The serializer must accept related fields as IDs for POST (using `PrimaryKeyRelatedField`).
- The client must send related fields as IDs, not nested objects.
- Metadata must be JSON matching the expected structure.

Following these steps ensures you can successfully add new Inventory items with complex metadata through the API.