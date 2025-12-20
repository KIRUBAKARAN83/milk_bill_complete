from django.db import models
from django.utils import timezone
from django.conf import settings
from decimal import Decimal
from django.db.models import Sum, F, ExpressionWrapper, DecimalField

PRICE_PER_LITRE = Decimal(str(getattr(settings, 'PRICE_PER_LITRE', 50)))


class Customer(models.Model):
    name = models.CharField(max_length=200, unique=True)

    # 🔒 Derived field (never manual)
    balance_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00'),
        editable=False
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    # ✅ SINGLE SOURCE OF TRUTH
    def recalculate_balance(self):
        amount_expr = ExpressionWrapper(
            F('quantity_ml') * PRICE_PER_LITRE / Decimal('1000'),
            output_field=DecimalField(max_digits=10, decimal_places=2)
        )

        total = (
            self.milk_entries
            .aggregate(total=Sum(amount_expr))
            .get('total') or Decimal('0.00')
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

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def litres(self):
        return Decimal(self.quantity_ml) / Decimal('1000')

    @property
    def amount(self):
        return self.litres * PRICE_PER_LITRE

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.customer.recalculate_balance()

    def delete(self, *args, **kwargs):
        customer = self.customer
        super().delete(*args, **kwargs)
        customer.recalculate_balance()

    def __str__(self):
        return f"{self.customer.name} | {self.date} | {self.quantity_ml} ml"
