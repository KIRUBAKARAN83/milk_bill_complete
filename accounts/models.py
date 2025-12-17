from django.db import models
from django.utils import timezone
from django.conf import settings
from decimal import Decimal
from django.db.models import Sum
from django.db.models.functions import Lower

PRICE_PER_LITRE = getattr(settings, 'PRICE_PER_LITRE', 50.0)


class Customer(models.Model):
    name = models.CharField(max_length=200)
    balance_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00')
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        constraints = [
            models.UniqueConstraint(
                Lower('name'),
                name='unique_customer_name_ci'
            )
        ]

    def __str__(self):
        return self.name

    # ✅ SINGLE SOURCE OF TRUTH
    # Balance = sum of non-deleted milk entry amounts
    def recalculate_balance(self):
        total = (
            self.milk_entries
            .filter(is_deleted=False)
            .aggregate(
                total=Sum(
                    models.F('quantity_ml') * Decimal(PRICE_PER_LITRE) / Decimal(1000)
                )
            )['total']
            or Decimal('0.00')
        )

        self.balance_amount = total
        self.save(update_fields=['balance_amount'])


class MilkEntry(models.Model):
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name='milk_entries'
    )

    date = models.DateField(default=timezone.now)
    quantity_ml = models.PositiveIntegerField(default=0)

    # Soft delete (used everywhere)
    is_deleted = models.BooleanField(default=False, db_index=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date']

    @property
    def litres(self):
        return Decimal(self.quantity_ml) / Decimal(1000)

    @property
    def amount(self):
        return self.litres * Decimal(PRICE_PER_LITRE)

    def __str__(self):
        return f"{self.customer.name} | {self.date} | {self.quantity_ml} ml"
