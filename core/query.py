import os

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.db.models import FloatField

from core.pos.models import Purchase

purchase = Purchase.objects.get(id=2)
purchase.subtotal = float(purchase.inventory_set.all().aggregate(result=Coalesce(Sum('subtotal'), 0.00, output_field=FloatField()))['result'])
print(purchase.subtotal)