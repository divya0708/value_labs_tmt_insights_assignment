# interview/inventory/pagination.py

from rest_framework.pagination import LimitOffsetPagination

class InventoryLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 3
    max_limit = 10