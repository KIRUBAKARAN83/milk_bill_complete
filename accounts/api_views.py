from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from decimal import Decimal

from .models import Customer, MilkEntry


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_entry(request):
    data = request.data

    quantity_ml = data.get('quantity_ml')
    date = data.get('date')
    customer_id = data.get('customer_id')
    customer_name = data.get('customer_name')

    if quantity_ml is None or date is None:
        return Response(
            {"error": "quantity_ml and date are required"},
            status=status.HTTP_400_BAD_REQUEST
        )

    if customer_id:
        customer = Customer.objects.filter(id=customer_id).first()
        if not customer:
            return Response({"error": "Invalid customer_id"}, status=400)
    elif customer_name:
        customer, _ = Customer.objects.get_or_create(name=customer_name.strip())
    else:
        return Response(
            {"error": "customer_id or customer_name required"},
            status=status.HTTP_400_BAD_REQUEST
        )

    entry = MilkEntry.objects.create(
        customer=customer,
        quantity_ml=int(quantity_ml),
        date=date
    )

    return Response({
        "message": "Entry created",
        "entry_id": entry.id,
        "customer": customer.name,
        "litres": float(entry.litres),
        "amount": float(entry.amount)
    }, status=status.HTTP_201_CREATED)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_entry(request, entry_id):
    entry = MilkEntry.objects.filter(id=entry_id).first()
    if not entry:
        return Response({"error": "Entry not found"}, status=404)

    entry.delete()
    return Response({"message": "Entry deleted"})
