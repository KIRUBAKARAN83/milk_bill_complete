from django.db import models
from django.utils import timezone
from django.conf import settings
from decimal import Decimal

PRICE_PER_LITRE = getattr(settings, 'PRICE_PER_LITRE', 50.0)


class Customer(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)
    balance_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.name or "Unknown Customer"

    class Meta:
        ordering = ['-created_at']

    # ✅ FIX: balance is now REAL, not stale
    def recalculate_balance(self):
        total = Decimal(0)
        for entry in self.milk_entries.filter(is_deleted=False):
            total += entry.amount
        self.balance_amount = total
        self.save(update_fields=['balance_amount'])


class MilkEntry(models.Model):
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name='milk_entries'
    )

    date = models.DateField(default=timezone.now)
    quantity_ml = models.IntegerField(default=0)

    # ✅ SOFT DELETE (USED EVERYWHERE IN VIEWS)
    is_deleted = models.BooleanField(default=False, db_index=True)

    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    @property
    def litres(self):
        return Decimal(self.quantity_ml) / Decimal(1000)

    @property
    def amount(self):
        return self.litres * Decimal(PRICE_PER_LITRE)

    def __str__(self):
        return f"{self.customer.name} - {self.date} - {self.quantity_ml}ml"

    class Meta:
        ordering = ['-date']
